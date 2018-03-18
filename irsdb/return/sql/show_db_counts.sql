
-- from: https://stackoverflow.com/a/2611745 -- from stats collector rather than live tables, but quick to run
SELECT schemaname,relname,n_live_tup 
  FROM pg_stat_user_tables 
  ORDER BY n_live_tup DESC;