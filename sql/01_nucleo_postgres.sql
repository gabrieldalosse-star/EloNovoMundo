-- Base relacional inicial para projeto NOVO Supabase/Neon.
-- Execute como proprietário do banco. Não é um sistema escolar completo.
-- Sem exclusões em cascata: preservar histórico institucional.
begin;
create table schools (
 id uuid primary key default gen_random_uuid(), name text not null, created_at timestamptz not null default now()
);
create table members (
 school_id uuid not null references schools(id), user_id text not null,
 role text not null check(role in ('admin','direction','coordinator','teacher','secretary')),
 active boolean not null default false, expires_at timestamptz,
 primary key(school_id,user_id)
);
create table classes (
 id uuid primary key default gen_random_uuid(), school_id uuid not null references schools(id),
 name text not null, segment text not null, academic_year integer not null,
 unique(school_id,id)
);
create table students (
 id uuid primary key default gen_random_uuid(), school_id uuid not null references schools(id),
 name text not null, external_id text, unique(school_id,id),unique(school_id,external_id)
);
create table enrollments (
 id uuid primary key default gen_random_uuid(), school_id uuid not null,
 class_id uuid not null, student_id uuid not null, starts_on date not null, ends_on date,
 foreign key(school_id,class_id) references classes(school_id,id),
 foreign key(school_id,student_id) references students(school_id,id),
 check(ends_on is null or ends_on>=starts_on),unique(school_id,class_id,student_id,starts_on),
 unique(school_id,class_id,id)
);
create table plans (
 id uuid primary key default gen_random_uuid(),school_id uuid not null,class_id uuid not null,author_id text not null,
 title text not null, status text not null default 'draft' check(status in ('draft','submitted','review','changes','resubmitted','approved')),
 body jsonb not null default '{}', revision integer not null default 0,
 foreign key(school_id,class_id) references classes(school_id,id),unique(school_id,class_id,id),unique(school_id,id)
);
create table plan_versions (
 id uuid primary key default gen_random_uuid(),school_id uuid not null,plan_id uuid not null,
 version integer not null,body jsonb not null,created_by text not null,created_at timestamptz not null default now(),
 foreign key(school_id,plan_id) references plans(school_id,id),unique(plan_id,version)
);
create table lessons (
 id uuid primary key default gen_random_uuid(),school_id uuid not null,class_id uuid not null,plan_id uuid,
 lesson_date date not null,slot text not null,
 state text not null default 'planned' check(state in ('planned','partial','completed','cancelled')),
 actual_content text,next_steps text,revision integer not null default 0,
 foreign key(school_id,class_id) references classes(school_id,id),
 foreign key(school_id,class_id,plan_id) references plans(school_id,class_id,id),
 unique(school_id,class_id,lesson_date,slot),unique(school_id,class_id,id)
);
create table attendance (
 school_id uuid not null,class_id uuid not null,lesson_id uuid not null,enrollment_id uuid not null,
 state text not null default 'unrecorded' check(state in ('unrecorded','present','absent','late')),
 foreign key(school_id,class_id,lesson_id) references lessons(school_id,class_id,id),
 foreign key(school_id,class_id,enrollment_id) references enrollments(school_id,class_id,id),
 primary key(lesson_id,enrollment_id)
);
create table audit_log (
 id uuid primary key default gen_random_uuid(),school_id uuid not null references schools(id),actor_id text not null,
 action text not null,reason text,before_data jsonb,after_data jsonb,created_at timestamptz not null default now()
);
-- Políticas serão criadas no arquivo 02 para Supabase. No Neon, acesso apenas pelo backend.
do $$ declare t text; begin
 foreach t in array array['schools','members','classes','students','enrollments','plans','plan_versions','lessons','attendance','audit_log'] loop
 execute format('alter table public.%I enable row level security',t);
 execute format('revoke all on table public.%I from public',t);
 end loop;
end $$;
commit;
