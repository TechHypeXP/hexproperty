import { promises as fs } from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { spawnSync } from 'child_process';

const execAsync = promisify(exec);

interface ValidationError {
  type: 'error' | 'warning';
  message: string;
  file?: string;
  line?: number;
}

interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationError[];
}

interface SpellCheckResult {
  word: string;
  suggestions: string[];
  line: number;
}

export class DocumentationValidator {
  private readonly docsDir: string;
  private readonly spellingExceptions: Set<string>;

  constructor(docsDir: string) {
    this.docsDir = docsDir;
    this.spellingExceptions = new Set([
      'api',
      'apis',
      'graphql',
      'grpc',
      'websocket',
      'websockets',
      'oauth',
      'oauth2',
      'oidc',
      'jwt',
      'kubernetes',
      'k8s',
      'istio',
      'prometheus',
      'grafana',
      'elasticsearch',
      'mongodb',
      'redis',
      'postgresql',
      'bigtable',
      'pubsub',
      'microservices',
    ]);
  }

  /**
   * Validates all documentation
   */
  async validateAll(): Promise<ValidationResult> {
    const results = await Promise.all([
      this.validateLinks(),
      this.validateExamples(),
      this.validateApiDocs(),
      this.validateArchitectureDocs(),
      this.validateSpelling(),
      this.validateFormatting(),
      this.validateImages(),
      this.validateConsistency(),
    ]);

    return results.reduce((acc, result) => ({
      valid: acc.valid && result.valid,
      errors: [...acc.errors, ...result.errors],
      warnings: [...acc.warnings, ...result.warnings]
    }), { valid: true, errors: [], warnings: [] });
  }

  /**
   * Validates documentation links
   */
  async validateLinks(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        
        // Check internal links
        const internalLinks = content.match(/\[([^\]]+)\]\(([^)]+)\)/g) || [];
        for (const link of internalLinks) {
          const [, , url] = /\[([^\]]+)\]\(([^)]+)\)/.exec(link) || [];
          if (url && !url.startsWith('http')) {
            const linkedFile = path.resolve(path.dirname(file), url);
            try {
              await fs.access(linkedFile);
            } catch {
              errors.push({
                type: 'error',
                message: `Broken internal link: ${url}`,
                file
              });
            }
          }
        }

        // Check external links
        const externalLinks = content.match(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g) || [];
        for (const link of externalLinks) {
          const [, , url] = /\[([^\]]+)\]\((https?:\/\/[^)]+)\)/.exec(link) || [];
          if (url) {
            try {
              const response = await fetch(url, { method: 'HEAD' });
              if (!response.ok) {
                warnings.push({
                  type: 'warning',
                  message: `Potentially broken external link: ${url}`,
                  file
                });
              }
            } catch {
              warnings.push({
                type: 'warning',
                message: `Unable to verify external link: ${url}`,
                file
              });
            }
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Link validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates spelling and grammar
   */
  async validateSpelling(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          const words = line.split(/\s+/);

          for (const word of words) {
            const cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
            if (cleanWord && !this.spellingExceptions.has(cleanWord)) {
              const result = spawnSync('hunspell', ['-d', 'en_US'], {
                input: cleanWord,
                encoding: 'utf-8'
              });

              if (result.status !== 0) {
                warnings.push({
                  type: 'warning',
                  message: `Possible spelling error: ${word}`,
                  file,
                  line: i + 1
                });
              }
            }
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Spelling validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates formatting consistency
   */
  async validateFormatting(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        const lines = content.split('\n');

        // Check heading hierarchy
        let lastHeadingLevel = 0;
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          const headingMatch = line.match(/^(#{1,6})\s/);
          if (headingMatch) {
            const level = headingMatch[1].length;
            if (lastHeadingLevel > 0 && level > lastHeadingLevel + 1) {
              warnings.push({
                type: 'warning',
                message: `Skipped heading level: from h${lastHeadingLevel} to h${level}`,
                file,
                line: i + 1
              });
            }
            lastHeadingLevel = level;
          }
        }

        // Check line length
        const maxLineLength = 120;
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (line.length > maxLineLength) {
            warnings.push({
              type: 'warning',
              message: `Line exceeds ${maxLineLength} characters`,
              file,
              line: i + 1
            });
          }
        }

        // Check code block formatting
        let inCodeBlock = false;
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (line.startsWith('```')) {
            inCodeBlock = !inCodeBlock;
            if (inCodeBlock && line.length === 3) {
              warnings.push({
                type: 'warning',
                message: 'Code block should specify language',
                file,
                line: i + 1
              });
            }
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Formatting validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates images and diagrams
   */
  async validateImages(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        
        // Check image references
        const imageRefs = content.match(/!\[([^\]]*)\]\(([^)]+)\)/g) || [];
        for (const ref of imageRefs) {
          const [, alt, src] = /!\[([^\]]*)\]\(([^)]+)\)/.exec(ref) || [];
          
          // Check alt text
          if (!alt) {
            warnings.push({
              type: 'warning',
              message: 'Image missing alt text',
              file
            });
          }

          // Check image file
          if (!src.startsWith('http')) {
            const imagePath = path.resolve(path.dirname(file), src);
            try {
              await fs.access(imagePath);
              
              // Check image size
              const stats = await fs.stat(imagePath);
              const maxSize = 5 * 1024 * 1024; // 5MB
              if (stats.size > maxSize) {
                warnings.push({
                  type: 'warning',
                  message: `Image file size exceeds 5MB: ${src}`,
                  file
                });
              }
            } catch {
              errors.push({
                type: 'error',
                message: `Missing image file: ${src}`,
                file
              });
            }
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Image validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates documentation consistency
   */
  async validateConsistency(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      const terms = new Map<string, string>();
      const patterns = new Map<string, RegExp>([
        ['HexProperty', /hex\s*property/i],
        ['PostgreSQL', /postgres(?:ql)?/i],
        ['JavaScript', /java\s*script/i],
        ['TypeScript', /type\s*script/i],
        ['WebSocket', /web\s*socket/i],
      ]);

      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];

          // Check term consistency
          for (const [correct, pattern] of patterns) {
            const match = line.match(pattern);
            if (match && match[0] !== correct) {
              warnings.push({
                type: 'warning',
                message: `Inconsistent term usage: "${match[0]}" should be "${correct}"`,
                file,
                line: i + 1
              });
            }
          }

          // Check for passive voice
          if (line.match(/\b(?:am|is|are|was|were|be|been|being)\s+\w+ed\b/i)) {
            warnings.push({
              type: 'warning',
              message: 'Consider using active voice',
              file,
              line: i + 1
            });
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Consistency validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates code examples in documentation
   */
  async validateExamples(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      const files = await this.findMarkdownFiles(this.docsDir);
      for (const file of files) {
        const content = await fs.readFile(file, 'utf-8');
        const codeBlocks = content.match(/```[^\n]*\n[\s\S]*?```/g) || [];

        for (const block of codeBlocks) {
          const [lang] = block.match(/```([^\n]*)/) || [];
          if (lang === '```typescript' || lang === '```javascript') {
            try {
              // Validate TypeScript/JavaScript syntax
              const code = block.replace(/```[^\n]*\n/, '').replace(/```$/, '');
              await execAsync(`npx tsc --noEmit --allowJs --checkJs false -t es2020 --strict false`, {
                input: code
              });
            } catch {
              errors.push({
                type: 'error',
                message: 'Invalid code example syntax',
                file
              });
            }
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Example validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates API documentation
   */
  async validateApiDocs(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      // Validate OpenAPI/Swagger documentation
      const swaggerPath = path.join(this.docsDir, 'api', 'swagger.json');
      try {
        const swagger = JSON.parse(await fs.readFile(swaggerPath, 'utf-8'));
        if (!swagger.openapi) {
          errors.push({
            type: 'error',
            message: 'Invalid OpenAPI specification',
            file: swaggerPath
          });
        }
      } catch {
        errors.push({
          type: 'error',
          message: 'Failed to parse OpenAPI specification',
          file: swaggerPath
        });
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `API documentation validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Validates architecture documentation
   */
  async validateArchitectureDocs(): Promise<ValidationResult> {
    try {
      const errors: ValidationError[] = [];
      const warnings: ValidationError[] = [];

      // Validate Mermaid diagrams
      const diagramsDir = path.join(this.docsDir, 'diagrams');
      const files = await fs.readdir(diagramsDir);
      
      for (const file of files) {
        if (file.endsWith('.mmd')) {
          try {
            const content = await fs.readFile(path.join(diagramsDir, file), 'utf-8');
            await execAsync(`mmdc -i ${path.join(diagramsDir, file)} -o /dev/null`);
          } catch {
            errors.push({
              type: 'error',
              message: 'Invalid Mermaid diagram syntax',
              file: path.join(diagramsDir, file)
            });
          }
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        warnings
      };
    } catch (error) {
      return {
        valid: false,
        errors: [{
          type: 'error',
          message: `Architecture documentation validation failed: ${error.message}`
        }],
        warnings: []
      };
    }
  }

  /**
   * Recursively finds all markdown files in a directory
   */
  private async findMarkdownFiles(dir: string): Promise<string[]> {
    const files = await fs.readdir(dir);
    const markdownFiles: string[] = [];

    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = await fs.stat(filePath);

      if (stat.isDirectory()) {
        markdownFiles.push(...await this.findMarkdownFiles(filePath));
      } else if (file.endsWith('.md')) {
        markdownFiles.push(filePath);
      }
    }

    return markdownFiles;
  }
}
