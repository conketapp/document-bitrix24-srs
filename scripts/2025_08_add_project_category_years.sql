-- Migration: Add project category versions by year
-- 1) Create base table if not exists changes required

-- Yearly categories (single source of truth)
CREATE TABLE IF NOT EXISTS project_category_years (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_code VARCHAR(50) NOT NULL,
    year SMALLINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    UNIQUE KEY uniq_category_year (category_code, year)
);

-- Projects table alteration: link to category by year
ALTER TABLE projects
    ADD COLUMN IF NOT EXISTS project_category_year_id INT NULL,
    ADD INDEX IF NOT EXISTS idx_project_category_year_id (project_category_year_id),
    ADD CONSTRAINT fk_projects_project_category_year
        FOREIGN KEY (project_category_year_id) REFERENCES project_category_years(id);

-- Cleanup legacy table if existed
DROP TABLE IF EXISTS project_categories;


