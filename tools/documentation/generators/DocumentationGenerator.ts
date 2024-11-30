import { promises as fs } from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface DocumentationConfig {
  source: string;
  output: string;
  format: 'markdown' | 'html' | 'pdf';
  templates: string[];
}

export interface GenerationResult {
  success: boolean;
  outputPath: string;
  errors?: string[];
}

export class DocumentationGenerator {
  private readonly config: DocumentationConfig;

  constructor(config: DocumentationConfig) {
    this.config = config;
  }

  /**
   * Generates documentation based on the provided configuration
   * @returns Promise<GenerationResult>
   */
  async generateDocs(): Promise<GenerationResult> {
    try {
      // Ensure output directory exists
      await fs.mkdir(this.config.output, { recursive: true });

      // Generate TypeDoc documentation
      await this.generateTypeDoc();

      // Generate API documentation
      await this.generateApiDocs();

      // Generate architecture diagrams
      await this.generateArchitectureDiagrams();

      return {
        success: true,
        outputPath: this.config.output
      };
    } catch (error) {
      return {
        success: false,
        outputPath: this.config.output,
        errors: [error.message]
      };
    }
  }

  /**
   * Generates TypeScript documentation using TypeDoc
   */
  private async generateTypeDoc(): Promise<void> {
    const typeDocConfig = {
      entryPoints: [this.config.source],
      out: path.join(this.config.output, 'api'),
      excludePrivate: true,
      excludeProtected: true,
      excludeExternals: true
    };

    await execAsync(`typedoc --options ${JSON.stringify(typeDocConfig)}`);
  }

  /**
   * Generates API documentation using OpenAPI/Swagger
   */
  private async generateApiDocs(): Promise<void> {
    const swaggerConfig = {
      definition: {
        openapi: '3.0.0',
        info: {
          title: 'HexProperty API',
          version: '1.0.0'
        }
      },
      apis: [`${this.config.source}/**/*.ts`]
    };

    await execAsync(`swagger-jsdoc -d ${JSON.stringify(swaggerConfig)} -o ${path.join(this.config.output, 'api', 'swagger.json')}`);
  }

  /**
   * Generates architecture diagrams using Mermaid
   */
  private async generateArchitectureDiagrams(): Promise<void> {
    const diagramsDir = path.join(this.config.source, 'docs', 'diagrams');
    const outputDir = path.join(this.config.output, 'architecture', 'diagrams');

    await fs.mkdir(outputDir, { recursive: true });

    const files = await fs.readdir(diagramsDir);
    for (const file of files) {
      if (file.endsWith('.mmd')) {
        await execAsync(`mmdc -i ${path.join(diagramsDir, file)} -o ${path.join(outputDir, file.replace('.mmd', '.svg'))}`);
      }
    }
  }

  /**
   * Validates generated documentation
   */
  async validateDocs(): Promise<boolean> {
    try {
      // Check if all required files exist
      const requiredFiles = [
        path.join(this.config.output, 'api', 'index.html'),
        path.join(this.config.output, 'api', 'swagger.json'),
        path.join(this.config.output, 'architecture', 'diagrams')
      ];

      for (const file of requiredFiles) {
        await fs.access(file);
      }

      // Validate links
      await this.validateLinks();

      return true;
    } catch (error) {
      console.error('Documentation validation failed:', error);
      return false;
    }
  }

  /**
   * Validates links in the documentation
   */
  private async validateLinks(): Promise<void> {
    // Implement link validation logic
    await execAsync(`broken-link-checker ${this.config.output} --recursive`);
  }

  /**
   * Deploys documentation to specified location
   */
  async deployDocs(): Promise<void> {
    // Implement deployment logic (e.g., to GitHub Pages)
    await execAsync(`gh-pages -d ${this.config.output}`);
  }
}
