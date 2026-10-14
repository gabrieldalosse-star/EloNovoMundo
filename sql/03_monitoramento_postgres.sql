-- Consultas somente para SQL Editor/backend autorizado, NÃO RPC pública.
-- Tamanho lógico/físico das relações do banco atual; não mede toda a fatura do provedor.
select current_database() as database,
 pg_database_size(current_database()) as used_bytes,
 pg_size_pretty(pg_database_size(current_database())) as formatted;
-- Dados + índices de cada tabela de usuário.
select schemaname,relname,
 pg_total_relation_size(relid) as total_bytes,
 pg_relation_size(relid) as table_bytes,
 pg_indexes_size(relid) as index_bytes
from pg_catalog.pg_statio_user_tables
order by total_bytes desc;
-- Exemplo de referência interna de 1 GiB, não limite contratado.
select round(pg_database_size(current_database())::numeric / 1073741824 * 100,2) as percent_of_internal_1gib;
