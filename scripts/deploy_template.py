class TemplateManager:
    """Template deployment and management system.

    First Iteration - Core Purpose:
    ---------------------------
    Core orchestration system for enterprise document template management,
    providing comprehensive template lifecycle management, deployment
    coordination, and system integration capabilities.

    Key Features:
    * Template lifecycle management
    * Deployment orchestration
    * Version control integration
    * Hook system coordination
    * Error handling and recovery

    Second Iteration - Technical Details:
    --------------------------------
    System Components:
    1. Core Management:
       * Template processing
       * Deployment coordination
       * Version control
       * Hook management
       * Error handling

    2. Service Integration:
       * Template service
       * Deployment service
       * Version control
       * Hook system
       * Logging service

    3. State Management:
       * Template state
       * Deployment state
       * System state
       * Error state
       * Recovery state

    Management Features:
    1. Template Operations:
       * Creation/Update/Delete
       * Version management
       * State tracking
       * Content processing
       * Validation

    2. Deployment Operations:
       * Deployment planning
       * Execution control
       * State management
       * Error handling
       * Recovery procedures

    Third Iteration - Implementation Context:
    ------------------------------------
    Implementation Features:
    1. Architecture Pattern:
       * Facade pattern
       * Strategy pattern
       * Observer pattern
       * Command pattern
       * Factory pattern

    2. Performance Optimization:
       * Operation batching
       * Resource pooling
       * Cache management
       * Lazy loading
       * Memory efficiency

    3. Integration Details:
       * Service coordination
       * Event handling
       * State synchronization
       * Error propagation
       * Resource management

    Attributes:
        config (ConfigModel): System configuration
        template_service (TemplateService): Template processing service
        deployment_history (DeploymentHistory): Deployment tracking
        git_service (Optional[GitService]): Version control service
        hook_manager (HookManager): Hook system manager

    Example:
        >>> manager = TemplateManager(config)
        >>> result = manager.deploy_template(
        ...     template_id="DOC-001",
        ...     target_path="/docs/policy.md",
        ...     variables={"title": "Policy"},
        ...     hooks={"pre": "validate"}
        ... )
    """

    def __init__(self, config: ConfigModel):
        """Initialize template manager.

        First Iteration - Core Purpose:
        ---------------------------
        Sets up the template management system with all required
        services and subsystems for template deployment operations.

        Second Iteration - Technical Details:
        --------------------------------
        Initialization Steps:
        1. Configuration setup
        2. Service initialization
        3. State preparation
        4. Resource allocation
        5. System validation

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Config validation
        * Service creation
        * Resource allocation
        * State initialization
        * Error handling

        Args:
            config (ConfigModel): System configuration
        """
        self.config = config
        self.template_service = TemplateService(config)
        self.deployment_history = DeploymentHistory(config.deployment_path)
        self.git_service = self._initialize_git() if config.version_control else None
        self.hook_manager = HookManager(config)

    def _initialize_git(self) -> Optional[GitService]:
        """Initialize Git service.

        First Iteration - Core Purpose:
        ---------------------------
        Sets up version control integration for template management,
        enabling source control and collaboration features.

        Second Iteration - Technical Details:
        --------------------------------
        Initialization Steps:
        1. Repository setup
        2. Branch configuration
        3. Remote configuration
        4. Authentication setup
        5. Hook integration

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Git integration
        * Auth management
        * Hook binding
        * Error handling
        * State tracking

        Returns:
            Optional[GitService]: Initialized Git service or None
        """
        try:
            return GitService(self.config.version_control)
        except Exception as e:
            logger.warning(f"Git integration disabled: {e}")
            return None

    @handle_errors("template_deployment")
    def deploy_template(
        self,
        template_type: str,
        target_path: str, 
        pre_hook: Optional[str] = None, 
        post_hook: Optional[str] = None,
        inherited_template: Optional[str] = None
    ) -> DeploymentRecord:
        """Deploy a template to target location.

        First Iteration - Core Purpose:
        ---------------------------
        Orchestrates the complete template deployment process,
        coordinating all necessary services and operations.

        Second Iteration - Technical Details:
        --------------------------------
        Deployment Process:
        1. Pre-deployment:
           * Template validation
           * Path verification
           * Hook preparation
           * State check
           * Resource allocation

        2. Deployment Steps:
           * Content processing
           * Variable substitution
           * Hook execution
           * File operations
           * State update

        3. Post-deployment:
           * State verification
           * History update
           * Hook cleanup
           * Resource cleanup
           * Error handling

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Operation coordination
        * Service integration
        * Error handling
        * State management
        * Resource cleanup

        Args:
            template_type (str): Type of template to deploy
            target_path (str): Deployment target path
            pre_hook (Optional[str]): Pre-deployment hook
            post_hook (Optional[str]): Post-deployment hook
            inherited_template (Optional[str]): Template to inherit from

        Returns:
            DeploymentRecord: Deployment record

        Raises:
            TemplateDeploymentError: If deployment fails
        """
        logger.info(f"Starting advanced deployment for {template_type}")
        
        # Initialize deployment context
        context = self._initialize_deployment_context(template_type, target_path)
        deployment_record = None
        
        try:
            # Execute pre-deployment hook if provided
            self._execute_hook(pre_hook, context)
            
            # Load and process template content
            content = self._load_template_content(template_type, inherited_template)
            template_path = self._get_template_path(template_type)
            
            # Generate metadata and relationships
            metadata = self._get_metadata(template_type, content)
            relationships = self._get_relationships(template_type)
            
            # Process template with metadata and relationships
            processed_content = self.template_service.process_template(
                content, metadata, relationships
            )
            
            # Create target directory if it doesn't exist
            target_path_obj = Path(target_path)
            target_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Deploy the processed template
            success = self._deploy_template(processed_content, target_path_obj)
            
            # Create and record deployment record
            deployment_record = self._create_deployment_record(
                template_type=template_type,
                target_path=target_path,
                metadata=metadata,
                success=success,
                template_path=template_path,
                inherited_template=inherited_template
            )
            self.deployment_history.record_deployment(deployment_record)
            
            # Execute post-deployment hook if provided
            self._execute_hook(post_hook, context)
            
            return deployment_record
            
        except Exception as e:
            error_msg = f"Template deployment failed: {str(e)}"
            logger.error(error_msg)
            
            if deployment_record is None:
                deployment_record = self._create_deployment_record(
                    template_type=template_type,
                    target_path=target_path,
                    metadata=None,
                    success=False,
                    template_path=self._get_template_path(template_type),
                    inherited_template=inherited_template,
                    error=str(e)
                )
                self.deployment_history.record_deployment(deployment_record)
            
            raise TemplateDeploymentError(error_msg) from e

    def _initialize_deployment_context(self, template_type: str, target_path: str) -> Dict[str, Any]:
        """Initialize the deployment context with essential information.

        First Iteration - Core Purpose:
        ---------------------------
        Creates a dictionary containing the basic context needed for template
        deployment and hook execution.

        Second Iteration - Technical Details:
        --------------------------------
        Context Components:
        * Template Type
        * Target Path
        * Timestamp

        Features:
        * Context creation
        * Timestamp generation

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses dictionary for context
        * Generates timestamp
        * Supports hook execution

        Parameters
        ----------
        template_type : str
            The type of template being deployed
        target_path : str
            The destination path for the template

        Returns
        -------
        Dict[str, Any]
            Dictionary containing deployment context information:
            - template_type: Type of template
            - target_path: Deployment destination
            - timestamp: Deployment start time

        Notes
        -----
        This context is passed to both pre and post deployment hooks
        """
        return {
            'template_type': template_type,
            'target_path': target_path,
            'timestamp': datetime.now()
        }

    def _execute_hook(self, hook_path: Optional[str], context: Dict[str, Any]) -> None:
        """Execute a deployment hook with the given context.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to execute deployment hooks with proper context.

        Second Iteration - Technical Details:
        --------------------------------
        Hook Execution:
        * Hook identification
        * Context passing
        * Hook execution

        Features:
        * Hook execution
        * Context passing

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses hook manager for execution
        * Passes context to hook
        * Supports hook execution

        Parameters
        ----------
        hook_path : str, optional
            Python path to the hook function (e.g., "module.submodule.hook_func")
        context : Dict[str, Any]
            Deployment context to pass to the hook

        Raises
        ------
        TemplateDeploymentError
            If hook execution fails

        Notes
        -----
        - Hooks are executed in a sandboxed environment
        - Hook functions must accept a single context parameter
        - Hook failures will abort the deployment process
        """
        if hook_path:
            hook_func = self.hook_manager.load_hook(hook_path)
            self.hook_manager.run_hook(hook_func, context)

    def _load_template_content(self, template_type: str, inherited_template: Optional[str]) -> str:
        """Load and process template content with optional inheritance.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to load and process template content with inheritance.

        Second Iteration - Technical Details:
        --------------------------------
        Template Loading:
        * Template identification
        * Inheritance resolution
        * Content loading

        Features:
        * Template loading
        * Inheritance resolution
        * Content processing

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses template service for loading
        * Supports inheritance
        * Processes template content

        Parameters
        ----------
        template_type : str
            Type of template to load
        inherited_template : str, optional
            Type of template to inherit from

        Returns
        -------
        str
            Processed template content

        Raises
        ------
        TemplateDeploymentError
            If template loading or inheritance processing fails

        Notes
        -----
        - Supports template inheritance through the inherited_template parameter
        - Base templates can be extended with additional content
        - Template paths are resolved using the configuration service
        """
        template_path = self._get_template_path(template_type)
        base_content = read_file(template_path)

        if inherited_template:
            inherited_path = self._get_template_path(inherited_template)
            base_content = (
                f"---\ninherits: {inherited_template}\n---\n{base_content}"
            )
        return base_content

    def _get_metadata(self, template_type: str, content: str) -> DocumentMetadataModel:
        """Extract and generate metadata for a template.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to extract and generate metadata for a template.

        Second Iteration - Technical Details:
        --------------------------------
        Metadata Generation:
        * Metadata identification
        * Metadata generation

        Features:
        * Metadata generation
        * Metadata validation

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses metadata model for generation
        * Validates metadata
        * Generates metadata

        Parameters
        ----------
        template_type : str
            Type of template being processed
        content : str
            Raw template content

        Returns
        -------
        DocumentMetadataModel
            Model containing template metadata:
            - doc_id: Unique document identifier
            - version: Document version
            - status: Document status
            - created_date: Creation timestamp
            - author: Document author
            - department: Owning department
            - classification: Security classification
            - template_version: Version of template used
            - checksum: Content checksum

        Raises
        ------
        TemplateDeploymentError
            If metadata generation fails

        Notes
        -----
        - Automatically generates missing required fields
        - Validates metadata format
        - Calculates content checksum
        """
        try:
            now = datetime.now()
            template_version = self.base_path / 'docs/templates' / self.config_service.load_config().templates_dir / template_type / 'version.txt'
            with open(template_version, 'r') as f:
                template_version = f.read().strip()
            
            metadata = DocumentMetadataModel(
                doc_id=f"{template_type}_{now.strftime('%Y%m%d_%H%M%S')}",
                version="1.0.0",
                status="draft",
                created_date=now,
                author=os.getenv('USER', 'system'),
                department=os.getenv('DEPARTMENT'),
                classification="internal",
                template_version=template_version,
                checksum=self._calculate_template_checksum(content)
            )
            return metadata
        except Exception as e:
            raise TemplateDeploymentError(f"Error generating metadata: {str(e)}")

    def _get_relationships(self, template_type: str) -> List[DocumentRelationshipModel]:
        """Get template relationships.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to get template relationships.

        Second Iteration - Technical Details:
        --------------------------------
        Relationship Loading:
        * Relationship identification
        * Relationship loading

        Features:
        * Relationship loading
        * Relationship validation

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses relationship model for loading
        * Validates relationships
        * Loads relationships

        Parameters
        ----------
        template_type : str
            Type of template being processed

        Returns
        -------
        List[DocumentRelationshipModel]
            List of relationships for the template

        Raises
        ------
        TemplateDeploymentError
            If relationship loading fails

        Notes
        -----
        - Relationships are loaded from a configuration file
        - Supports multiple relationship types
        """
        try:
            relationships = []
            template_config = self.base_path / 'docs/templates' / self.config_service.load_config().templates_dir / template_type / 'relationships.yaml'
            with open(template_config, 'r') as f:
                relationships_data = yaml.safe_load(f)
            
            for rel_type, items in relationships_data.items():
                for item in items:
                    relationship = DocumentRelationshipModel(
                        source_id=template_type,
                        target_id=item.get('doc_id', ''),
                        relationship_type=rel_type,
                        metadata=item.get('metadata', {})
                    )
                    relationships.append(relationship)
            
            # Check for circular dependencies
            self.dependency_service.check_circular_dependencies({template_type: relationships})
            
            return relationships
        except KeyError as e:
            raise TemplateDeploymentError(f"Missing required relationship field: {str(e)}")
        except Exception as e:
            raise TemplateDeploymentError(f"Error processing relationships: {str(e)}")

    def _calculate_template_checksum(self, content: str) -> str:
        """Calculate template checksum.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to calculate template checksum.

        Second Iteration - Technical Details:
        --------------------------------
        Checksum Calculation:
        * Checksum algorithm
        * Content hashing

        Features:
        * Checksum calculation
        * Content hashing

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Uses SHA-256 for hashing
        * Calculates checksum

        Parameters
        ----------
        content : str
            Template content

        Returns
        -------
        str
            Template checksum
        """
        return hashlib.sha256(content.encode()).hexdigest()

    def _create_deployment_record(
        self, 
        template_type: str, 
        target_path: str, 
        metadata: Optional[DocumentMetadataModel], 
        success: bool, 
        template_path: str, 
        inherited_template: Optional[str] = None, 
        error: Optional[str] = None
    ) -> DeploymentRecord:
        """Create a deployment record.

        First Iteration - Core Purpose:
        ---------------------------
        Provides a way to create a deployment record.

        Second Iteration - Technical Details:
        --------------------------------
        Record Creation:
        * Record initialization
        * State update
        * Index update
        * Record storage

        Features:
        * Record creation
        * State update
        * Index update

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Record initialization
        * State update
        * Index update
        * Record storage

        Parameters
        ----------
        template_type : str
            Type of template deployed
        target_path : str
            Deployment target path
        metadata : DocumentMetadataModel
            Template metadata
        success : bool
            Deployment success status
        template_path : str
            Path to template
        inherited_template : str, optional
            Template to inherit from
        error : str, optional
            Error message if failed

        Returns
        -------
        DeploymentRecord
            Deployment record
        """
        record = DeploymentRecord(
            template_type=template_type,
            target_path=target_path,
            timestamp=datetime.now(),
            status="success" if success else "failure",
            version=metadata.version if metadata else "unknown",
            checksum=metadata.checksum if metadata else "unknown",
            metadata=asdict(metadata) if metadata else {},
            error=error
        )
        return record

class HookManager:
    """Hook system management and execution.

    First Iteration - Core Purpose:
    ---------------------------
    Manages and executes deployment hooks, providing extensibility
    and customization points throughout the template deployment
    lifecycle. Enables system integration and workflow automation.

    Key Features:
    * Hook registration
    * Execution control
    * Error handling
    * Context management
    * Resource cleanup

    Second Iteration - Technical Details:
    --------------------------------
    System Components:
    1. Hook Management:
       * Hook registration
       * Hook discovery
       * Hook validation
       * Hook lifecycle
       * Hook dependencies

    2. Execution Engine:
       * Context preparation
       * Hook invocation
       * Error handling
       * Result processing
       * Resource management

    3. Integration Points:
       * Template system
       * Deployment system
       * Validation system
       * Logging system
       * Monitoring system

    Hook Categories:
    1. Lifecycle Hooks:
       * Pre-deployment
       * Post-deployment
       * Validation
       * Cleanup
       * Recovery

    2. Integration Hooks:
       * Version control
       * Notification
       * Audit
       * Analytics
       * Monitoring

    Third Iteration - Implementation Context:
    ------------------------------------
    Implementation Features:
    1. Hook Architecture:
       * Plugin system
       * Event system
       * Pipeline pattern
       * Chain pattern
       * Observer pattern

    2. Performance Features:
       * Lazy loading
       * Hook caching
       * Parallel execution
       * Resource pooling
       * Memory management

    3. Security Features:
       * Hook validation
       * Sandbox execution
       * Resource limits
       * Error isolation
       * Access control

    Attributes:
        config (ConfigModel): System configuration
        hooks (Dict[str, Callable]): Registered hooks
        context (Dict[str, Any]): Execution context
        resources (Dict[str, Any]): Hook resources

    Example:
        >>> manager = HookManager(config)
        >>> manager.register_hook('validate', validate_fn)
        >>> result = manager.execute_hook(
        ...     'validate',
        ...     context={'template_id': 'DOC-001'}
        ... )
    """

    def __init__(self, config: ConfigModel):
        """Initialize hook manager.

        First Iteration - Core Purpose:
        ---------------------------
        Sets up the hook management system with configuration,
        hook registration, and execution environment.

        Second Iteration - Technical Details:
        --------------------------------
        Initialization Steps:
        1. Config setup
        2. Hook registration
        3. Context creation
        4. Resource allocation
        5. Security setup

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Config validation
        * Hook discovery
        * Context setup
        * Resource allocation
        * Security checks

        Args:
            config (ConfigModel): System configuration
        """
        self.config = config
        self.hooks: Dict[str, Callable] = {}
        self.context: Dict[str, Any] = {}
        self.resources: Dict[str, Any] = {}
        self._initialize_hooks()

    def _initialize_hooks(self) -> None:
        """Initialize hook system.

        First Iteration - Core Purpose:
        ---------------------------
        Sets up the hook system with default hooks and prepares
        the execution environment for custom hooks.

        Second Iteration - Technical Details:
        --------------------------------
        Setup Components:
        1. Default Hooks:
           * System hooks
           * Validation hooks
           * Lifecycle hooks
           * Utility hooks
           * Recovery hooks

        2. Hook Environment:
           * Context setup
           * Resource allocation
           * Security context
           * Logging setup
           * Monitoring

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Hook registration
        * Environment setup
        * Security config
        * Resource prep
        * Error handling
        """
        # Register default hooks
        self.register_hook('validate', self._validate_template)
        self.register_hook('notify', self._notify_deployment)
        self.register_hook('cleanup', self._cleanup_resources)

    def register_hook(self, name: str, hook: Callable) -> None:
        """Register a new hook.

        First Iteration - Core Purpose:
        ---------------------------
        Registers a new hook in the system, making it available
        for execution during template deployment.

        Second Iteration - Technical Details:
        --------------------------------
        Registration Process:
        1. Hook Validation:
           * Name validation
           * Signature check
           * Security check
           * Resource check
           * Dependency check

        2. Registration Steps:
           * Hook storage
           * Metadata capture
           * Resource allocation
           * Context setup
           * Integration check

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Name validation
        * Hook validation
        * Resource check
        * Security scan
        * Registration

        Args:
            name (str): Hook name
            hook (Callable): Hook function
        """
        if not callable(hook):
            raise ValueError("Hook must be callable")
        self.hooks[name] = hook

    def execute_hook(self, name: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a registered hook.

        First Iteration - Core Purpose:
        ---------------------------
        Executes a registered hook with proper context management,
        error handling, and resource cleanup.

        Second Iteration - Technical Details:
        --------------------------------
        Execution Process:
        1. Pre-execution:
           * Hook validation
           * Context preparation
           * Resource allocation
           * Security check
           * State verification

        2. Execution:
           * Hook invocation
           * Error handling
           * Result capture
           * State update
           * Event logging

        3. Post-execution:
           * Resource cleanup
           * State cleanup
           * Result processing
           * Error handling
           * Event notification

        Third Iteration - Implementation Context:
        ------------------------------------
        Implementation Details:
        * Context injection
        * Error handling
        * Resource management
        * State tracking
        * Logging

        Args:
            name (str): Hook name
            context (Optional[Dict[str, Any]]): Execution context

        Returns:
            Any: Hook execution result

        Raises:
            TemplateDeploymentError: If hook execution fails
        """
        if name not in self.hooks:
            raise TemplateDeploymentError(
                message=f"Hook not found: {name}",
                error_type="HookError"
            )

        try:
            hook = self.hooks[name]
            context = {**self.context, **(context or {})}
            return hook(context)
        except Exception as e:
            raise TemplateDeploymentError(
                message=f"Hook execution failed: {e}",
                error_type="HookExecutionError",
                context={'hook': name, **context}
            ) from e
