/**
 * Database integration tests
 */
import { DatabaseManager } from './database';
import { Pool } from 'pg';

describe('DatabaseManager', () => {
  let db: DatabaseManager;
  let pool: Pool;

  beforeAll(async () => {
    db = DatabaseManager.getInstance();
    pool = db.getPool();
  });

  afterAll(async () => {
    await db.close();
  });

  test('should connect to database successfully', async () => {
    const result = await pool.query('SELECT 1 as test');
    expect(result.rows[0].test).toBe(1);
  });

  test('should throw error on missing config', () => {
    // Test with invalid config would go here
    expect(() => {
      // Simulate missing config
    }).toThrow('Database config missing');
  });

  test('should be singleton', () => {
    const db2 = DatabaseManager.getInstance();
    expect(db).toBe(db2);
  });
});
