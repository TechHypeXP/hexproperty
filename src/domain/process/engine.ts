import { 
  BusinessProcess,
  BusinessProcessStep,
  ProcessContext,
  ProcessResult,
  ProcessConfiguration 
} from '@/types/process';

export class ProcessEngine {
  private processes: Map<string, BusinessProcess<any, any>> = new Map();
  private configurations: Map<string, ProcessConfiguration> = new Map();

  registerProcess(name: string, process: BusinessProcess<any, any>, config: ProcessConfiguration) {
    this.processes.set(name, process);
    this.configurations.set(name, config);
  }

  async executeProcess<TInput, TOutput>(
    processName: string,
    input: TInput
  ): Promise<ProcessResult<TOutput>> {
    const process = this.processes.get(processName);
    const config = this.configurations.get(processName);

    if (!process || !config) {
      throw new Error(`Process ${processName} not found`);
    }

    // Create initial context
    const context: ProcessContext<TInput> = {
      input,
      state: {},
      metadata: {
        processId: crypto.randomUUID(),
        startedAt: new Date(),
        completedSteps: []
      }
    };

    // Validate input
    const validationResult = await process.validate(input);
    if (!validationResult.success) {
      return {
        success: false,
        error: new Error(validationResult.errors?.join(', ')),
        context
      };
    }

    // Execute steps in order
    for (const stepName of config.steps.order) {
      const step = process.steps.find(s => s.name === stepName);
      if (!step) continue;

      // Check if step should be executed
      if (!this.shouldExecuteStep(step, context, config)) {
        continue;
      }

      // Execute step
      context.metadata.currentStep = stepName;
      const stepResult = await this.executeStep(step, context);

      if (!stepResult.success) {
        return stepResult;
      }

      // Update context with step results
      context.state = { ...context.state, ...stepResult.data };
      context.metadata.completedSteps.push(stepName);
    }

    return {
      success: true,
      data: context.state as TOutput,
      context
    };
  }

  private shouldExecuteStep(
    step: BusinessProcessStep,
    context: ProcessContext,
    config: ProcessConfiguration
  ): boolean {
    const stepConfig = config.steps.conditional[step.name];
    
    if (stepConfig && !stepConfig.enabled) {
      return false;
    }

    if (step.condition && !step.condition(context)) {
      return false;
    }

    if (stepConfig?.condition && !stepConfig.condition(context)) {
      return false;
    }

    return true;
  }

  private async executeStep(
    step: BusinessProcessStep,
    context: ProcessContext
  ): Promise<ProcessResult<any>> {
    try {
      return await step.execute(context);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Step execution failed'),
        context
      };
    }
  }
}
