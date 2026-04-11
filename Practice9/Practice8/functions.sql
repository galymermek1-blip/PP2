CREATE OR REPLACE FUNCTION search_contacts(pattern_text TEXT)
RETURNS TABLE(username VARCHAR, phone VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT p.username, p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || pattern_text || '%'
       OR p.phone ILIKE '%' || pattern_text || '%';
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.username, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT p_limit OFFSET p_offset;
END;
$$
LANGUAGE plpgsql;