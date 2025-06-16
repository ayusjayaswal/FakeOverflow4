create extension if not exists pg_trgm;
create extension if not exists btree_gin;
create table if not exists users (
    id serial primary key,
    username varchar(50) unique not null,
    email varchar(100) unique not null,
    password_hash varchar(255) not null,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    is_active boolean default true
);
create table if not exists discussions (
    id serial primary key,
    title varchar(255) not null,
    content text not null,
    tags text[] default '{}',
    user_id integer not null references users(id) on delete cascade,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    is_active boolean default true
);
create table if not exists comments (
    id serial primary key,
    content text not null,
    user_id integer not null references users(id) on delete cascade,
    discussion_id integer not null references discussions(id) on delete cascade,
    parent_comment_id integer references comments(id) on delete cascade,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    is_active boolean default true
);
create index if not exists idx_users_username on users(username);
create index if not exists idx_users_email on users(email);
create index if not exists idx_users_is_active on users(is_active);

create index if not exists idx_discussions_user_id on discussions(user_id);
create index if not exists idx_discussions_created_at on discussions(created_at desc);
create index if not exists idx_discussions_is_active on discussions(is_active);
create index if not exists idx_discussions_tags on discussions using gin(tags);

create index if not exists idx_comments_user_id on comments(user_id);
create index if not exists idx_comments_discussion_id on comments(discussion_id);
create index if not exists idx_comments_parent_comment_id on comments(parent_comment_id);
create index if not exists idx_comments_is_active on comments(is_active);

create index if not exists idx_discussions_title_trgm on discussions using gin(title gin_trgm_ops);
create index if not exists idx_discussions_content_trgm on discussions using gin(content gin_trgm_ops);
create index if not exists idx_comments_content_trgm on comments using gin(content gin_trgm_ops);

create index if not exists idx_discussions_search on discussions using gin(
    to_tsvector('english', title || ' ' || content)
);

create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language 'plpgsql';

-- create triggers for updated_at
create or replace trigger update_users_updated_at
    before update on users
    for each row
    execute function update_updated_at_column();

create or replace trigger update_discussions_updated_at
    before update on discussions
    for each row
    execute function update_updated_at_column();

create or replace trigger update_comments_updated_at
    before update on comments
    for each row
    execute function update_updated_at_column();

-- grant necessary permissions 
-- grant all privileges on all tables in schema public to user;
-- grant all privileges on all sequences in schema public to user;
