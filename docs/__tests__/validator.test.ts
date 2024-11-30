import { DocumentationValidator } from '../tools/documentation/validators/validate';
import path from 'path';

describe('DocumentationValidator', () => {
  const validator = new DocumentationValidator(path.join(__dirname, '..'));

  describe('validateLinks', () => {
    it('should detect broken internal links', async () => {
      const result = await validator.validateLinks();
      expect(result.valid).toBeDefined();
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });

  describe('validateExamples', () => {
    it('should validate code examples', async () => {
      const result = await validator.validateExamples();
      expect(result.valid).toBeDefined();
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });

  describe('validateApiDocs', () => {
    it('should validate OpenAPI specification', async () => {
      const result = await validator.validateApiDocs();
      expect(result.valid).toBeDefined();
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });

  describe('validateArchitectureDocs', () => {
    it('should validate Mermaid diagrams', async () => {
      const result = await validator.validateArchitectureDocs();
      expect(result.valid).toBeDefined();
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });

  describe('validateAll', () => {
    it('should run all validations', async () => {
      const result = await validator.validateAll();
      expect(result.valid).toBeDefined();
      expect(Array.isArray(result.errors)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });
});
