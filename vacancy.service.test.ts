/**
 * VacancyService unit tests
 */
import { VacancyService } from './vacancy.service';

jest.mock('axios');

describe('VacancyService', () => {
  let service: VacancyService;

  beforeAll(() => {
    process.env.HH_API_KEY = 'test-key';
    service = VacancyService.getInstance();
  });

  test('should be singleton', () => {
    const service2 = VacancyService.getInstance();
    expect(service).toBe(service2);
  });

  test('should throw error without API key', () => {
    delete process.env.HH_API_KEY;
    expect(() => VacancyService.getInstance()).toThrow('HH_API_KEY');
  });
});