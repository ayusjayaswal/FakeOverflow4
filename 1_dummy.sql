-- Insert users
INSERT INTO users (id, username, email, password_hash) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Oggy', 'oggy@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewf4RKzjPVnJxn4W'),
('550e8400-e29b-41d4-a716-446655440002', 'Shinchan', 'shinchan@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewf4RKzjPVnJxn4W'),
('550e8400-e29b-41d4-a716-446655440003', 'Nobita', 'nobita@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewf4RKzjPVnJxn4W'),
('550e8400-e29b-41d4-a716-446655440004', 'Jack', 'jack@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewf4RKzjPVnJxn4W');

-- Insert discussions
INSERT INTO discussions (id, title, content, tags, user_id, created_at) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'What are the best pizza toppings?', 
'I''ve been thinking about this for ages. I personally love pepperoni and mushrooms, but my friend says pineapple is the way to go. What do you all think? Are there any unconventional toppings that actually taste amazing?',
ARRAY['food', 'pizza', 'debate'], 
'550e8400-e29b-41d4-a716-446655440001', 
NOW() - INTERVAL '3 days'),

('660e8400-e29b-41d4-a716-446655440002', 'How do you start your perfect morning?', 
'I''m trying to build a better morning routine. Right now I just roll out of bed and grab coffee, but I feel like I''m missing out on setting a good tone for the day. What does your ideal morning look like?',
ARRAY['lifestyle', 'routine', 'wellness'], 
'550e8400-e29b-41d4-a716-446655440002', 
NOW() - INTERVAL '2 days'),

('660e8400-e29b-41d4-a716-446655440003', 'What''s your all-time favorite childhood cartoon?', 
'Been feeling nostalgic lately and rewatching some old cartoons. There''s something magical about the shows we loved as kids. They just don''t make them like they used to! What cartoon brings back the best memories for you?',
ARRAY['nostalgia', 'cartoons', 'childhood'], 
'550e8400-e29b-41d4-a716-446655440003', 
NOW() - INTERVAL '1 day'),

('660e8400-e29b-41d4-a716-446655440004', 'If money wasn''t an issue, where would you go?', 
'I''ve been daydreaming about travel lately. If I could go anywhere in the world without worrying about budget, I think I''d love to explore the northern lights in Iceland or maybe go on a safari in Kenya. Where would your dream vacation take you?',
ARRAY['travel', 'vacation', 'dreams'], 
'550e8400-e29b-41d4-a716-446655440004', 
NOW() - INTERVAL '6 hours');

INSERT INTO comments (content, user_id, discussion_id, created_at) VALUES
('Pineapple on pizza is actually delicious! Don''t knock it till you try it with some jalapeños for that sweet and spicy combo.', 
'550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 days 20 hours'),

('I''m team pepperoni all the way! But have you tried adding some fresh basil and garlic? Game changer!', 
'550e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 days 18 hours'),

('Okay, hear me out - BBQ chicken with red onions and cilantro. It''s like a party in your mouth!', 
'550e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 days 15 hours');

-- Get the comment IDs for replies (we'll use these in the replies)
-- Note: In practice, you'd need to get these IDs from the inserted comments above
-- For this demo, we'll create replies separately

INSERT INTO comments (content, user_id, discussion_id, created_at) VALUES
('I start with 10 minutes of stretching, then make tea while listening to some calm music. It really sets a peaceful mood for the whole day!', 
'550e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '1 day 20 hours'),

('My morning ritual is coffee first, then I write in my journal for about 5 minutes. Just getting thoughts out of my head helps me focus.', 
'550e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '1 day 18 hours'),

('I''ve been trying to wake up 30 minutes earlier just to sit outside with my coffee. Even 5 minutes of fresh air makes such a difference!', 
'550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '1 day 16 hours');

INSERT INTO comments (content, user_id, discussion_id, created_at) VALUES
('Tom and Jerry was my absolute favorite! No dialogue needed, just pure slapstick comedy gold. I still laugh at those episodes today.', 
'550e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003', NOW() - INTERVAL '20 hours'),

('Scooby-Doo was everything to me as a kid! I loved trying to solve the mysteries before the gang did. Plus, who doesn''t love Scooby Snacks?', 
'550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440003', NOW() - INTERVAL '18 hours'),

('Dragon Ball Z got me so hyped as a kid! The fight scenes were incredible and I spent way too much time trying to go Super Saiyan in my backyard.', 
'550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440003', NOW() - INTERVAL '15 hours');

INSERT INTO comments (content, user_id, discussion_id, created_at) VALUES
('Japan has been on my bucket list forever! I want to experience cherry blossom season, try authentic ramen, and visit all the beautiful temples.', 
'550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '4 hours'),

('I''d love to do a European backpacking trip - Italy, France, Spain, just hopping from city to city trying amazing food and seeing incredible art!', 
'550e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '3 hours'),

('New Zealand for me! The landscapes look absolutely breathtaking. I want to go bungee jumping and see those glowworm caves!', 
'550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '2 hours');

-- Now add some replies using dynamic parent comment selection
-- Note: Since we can't easily reference the auto-generated IDs, we'll add replies in a simpler way

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'Wait, pineapple AND jalapeños? That actually sounds intriguing. I might have to give it a shot!',
    '550e8400-e29b-41d4-a716-446655440001',
    '660e8400-e29b-41d4-a716-446655440001',
    c.id,
    NOW() - INTERVAL '2 days 19 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440001' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%pineapple%jalapeños%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'BBQ chicken pizza is SO underrated! I love adding some pineapple to that too for the ultimate sweet and savory experience.',
    '550e8400-e29b-41d4-a716-446655440002',
    '660e8400-e29b-41d4-a716-446655440001',
    c.id,
    NOW() - INTERVAL '2 days 14 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440001' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%BBQ chicken%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'Stretching sounds amazing! I always feel so stiff in the mornings. What kind of stretches do you do?',
    '550e8400-e29b-41d4-a716-446655440002',
    '660e8400-e29b-41d4-a716-446655440002',
    c.id,
    NOW() - INTERVAL '1 day 19 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440002' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%stretching%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'Journaling is such a great idea! I tried it once but couldn''t stick with it. Any tips for making it a habit?',
    '550e8400-e29b-41d4-a716-446655440001',
    '660e8400-e29b-41d4-a716-446655440002',
    c.id,
    NOW() - INTERVAL '1 day 17 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440002' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%journal%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'YES! Tom and Jerry is timeless. My kids watch it now and they crack up just as much as I did. True comedy genius.',
    '550e8400-e29b-41d4-a716-446655440003',
    '660e8400-e29b-41d4-a716-446655440003',
    c.id,
    NOW() - INTERVAL '19 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440003' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%Tom and Jerry%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'Haha, I totally tried the Super Saiyan thing too! Standing in front of the mirror yelling and trying to make my hair stand up. Good times!',
    '550e8400-e29b-41d4-a716-446655440004',
    '660e8400-e29b-41d4-a716-446655440003',
    c.id,
    NOW() - INTERVAL '14 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440003' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%Super Saiyan%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'Japan in cherry blossom season would be magical! I''ve heard the food alone is worth the trip. Have you looked into any specific cities?',
    '550e8400-e29b-41d4-a716-446655440004',
    '660e8400-e29b-41d4-a716-446655440004',
    c.id,
    NOW() - INTERVAL '3.5 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440004' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%Japan%'
LIMIT 1;

INSERT INTO comments (content, user_id, discussion_id, parent_comment_id, created_at) 
SELECT 
    'European backpacking sounds incredible! I''ve always wanted to see the Louvre in person. How long do you think you''d want to spend in each country?',
    '550e8400-e29b-41d4-a716-446655440002',
    '660e8400-e29b-41d4-a716-446655440004',
    c.id,
    NOW() - INTERVAL '2.5 hours'
FROM comments c 
WHERE c.discussion_id = '660e8400-e29b-41d4-a716-446655440004' 
  AND c.parent_comment_id IS NULL 
  AND c.content LIKE '%European%'
LIMIT 1;
