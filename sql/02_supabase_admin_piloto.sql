-- SUPABASE SOMENTE. Executar depois do 01 em projeto de teste NOVO.
-- Base restrita a admins. Não libera docentes e não implementa o fluxo institucional completo.
begin;
create schema if not exists private;
revoke all on schema private from public;
grant usage on schema private to authenticated;
create or replace function private.is_school_admin(sid uuid)
returns boolean language sql stable security definer set search_path='' as $$
 select exists(select 1 from public.members m where m.school_id=sid and m.user_id=auth.uid()::text and m.role='admin' and m.active and (m.expires_at is null or m.expires_at>now()));
$$;
revoke all on function private.is_school_admin(uuid) from public;
grant execute on function private.is_school_admin(uuid) to authenticated;
-- Cadastro/alteração de membros somente pelo operador/servidor. Usuário não se promove.
grant select on schools,members to authenticated;
create policy schools_admin_read on schools for select to authenticated using(private.is_school_admin(id));
create policy members_admin_read on members for select to authenticated using(private.is_school_admin(school_id));
do $$ declare t text; begin
 foreach t in array array['classes','students','enrollments','plans','lessons','attendance'] loop
 execute format('grant select,insert,update on table public.%I to authenticated',t);
 execute format('create policy admin_select on public.%I for select to authenticated using(private.is_school_admin(school_id))',t);
 execute format('create policy admin_insert on public.%I for insert to authenticated with check(private.is_school_admin(school_id))',t);
 execute format('create policy admin_update on public.%I for update to authenticated using(private.is_school_admin(school_id)) with check(private.is_school_admin(school_id))',t);
 end loop;
end $$;
-- Versões e auditoria: somente leitura; escrita deve ser feita em operação transacional no backend.
grant select on plan_versions,audit_log to authenticated;
create policy versions_admin_read on plan_versions for select to authenticated using(private.is_school_admin(school_id));
create policy audit_admin_read on audit_log for select to authenticated using(private.is_school_admin(school_id));
commit;
