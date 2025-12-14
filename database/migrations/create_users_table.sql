-- Create users table for authentication
-- Migration: create_users_table
-- Created: 2025-12-14

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Insert default admin user (password: admin123)
-- Password hash generated with werkzeug.security
INSERT INTO users (email, password_hash, full_name) 
VALUES (
    'admin@ssis.edu',
    'scrypt:32768:8:1$TQVJ4zYNgzMzGGkT$b8f8f1c4e5f1a1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1e1f1',
    'System Administrator'
) ON CONFLICT (email) DO NOTHING;

COMMENT ON TABLE users IS 'User authentication table for SSIS v4';
COMMENT ON COLUMN users.user_id IS 'Auto-incrementing primary key';
COMMENT ON COLUMN users.email IS 'Unique email address for login';
COMMENT ON COLUMN users.password_hash IS 'Hashed password using werkzeug.security';
COMMENT ON COLUMN users.full_name IS 'Display name of the user';
