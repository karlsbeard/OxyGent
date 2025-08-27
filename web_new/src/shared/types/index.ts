// Core domain types
export interface Agent {
  id: string;
  name: string;
  type: 'react' | 'chat' | 'workflow' | 'parallel';
  status: 'idle' | 'working' | 'error' | 'completed';
  description: string;
  tools: string[];
  children?: Agent[];
  isRemote?: boolean;
  path?: string[];
}

export interface Message {
  id: string;
  role: 'user' | 'agent' | 'system';
  content: string;
  timestamp: Date;
  attachments?: Attachment[];
  at?: string; // @mention functionality
  agentId?: string;
}

export interface Attachment {
  name: string;
  size: number;
  type: string;
  url?: string;
  serverName?: string;
}

export interface ExecutionNode {
  node_id: string;
  caller: string;
  callee: string;
  node_type: 'agent' | 'tool' | 'llm' | 'flow';
  status: 'pending' | 'running' | 'completed' | 'error';
  trace_id: string;
  create_time: string;
  input: {
    class_attr?: Record<string, unknown>;
    arguments?: Record<string, unknown>;
  };
  output?: string;
  children?: ExecutionNode[];
  father_node_id?: string;
  pre_id?: string;
  next_id?: string;
}

export interface WebSocketMessage {
  type: 'tool_call' | 'observation' | 'status_update';
  content: {
    caller?: string;
    callee?: string;
    caller_category?: 'agent' | 'tool' | 'llm' | 'user';
    callee_category?: 'agent' | 'tool' | 'llm' | 'user';
    call_stack?: string[];
    node_id?: string;
    output?: string | Record<string, unknown>;
    arguments?: Record<string, unknown>;
    current_trace_id?: string;
  };
  trace_id: string;
  timestamp: Date;
}

export interface ChatHistory {
  agent_id_dict: Record<string, number>;
  agent_organization: Agent;
  answer: Message[];
  agent_log: Record<string, unknown>;
  tool_call: Record<string, string>;
}

// UI State types
export interface LayoutState {
  sidebarCollapsed: boolean;
  rightPanelVisible: boolean;
  currentView: 'dashboard' | 'node-detail';
  selectedNodeId: string | null;
}

export interface ConnectionState {
  isConnected: boolean;
  connectionError: string | null;
  reconnectAttempts: number;
}

// API Response types
export interface ApiResponse<T = unknown> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface OrganizationResponse {
  id_dict: Record<string, number>;
  organization: Agent;
}

export interface WelcomeMessageResponse {
  welcome_message: string;
}

export interface ScriptResponse {
  scripts: string[];
}

export interface NodeResponse {
  node: ExecutionNode;
  data_range_map?: Record<string, unknown>;
  pre_id?: string;
  next_id?: string;
}

// Configuration types
export interface AppConfig {
  apiBaseUrl: string;
  wsUrl: string;
  maxFileSize: number;
  allowedFileTypes: string[];
  reconnectInterval: number;
  maxReconnectAttempts: number;
}

// Utility types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type Without<T, U> = { [P in Exclude<keyof T, keyof U>]?: never };
export type XOR<T, U> = T | U extends object ? (Without<T, U> & U) | (Without<U, T> & T) : T | U;

// Event types for custom hooks
export interface AgentUpdateEvent {
  agent: Agent;
  type: 'status' | 'data' | 'structure';
}

export interface MessageEvent {
  message: Message;
  type: 'new' | 'update' | 'delete';
}

// Form types
export interface FileUploadForm {
  files: File[];
  uploadProgress: Record<string, number>;
  uploadStatus: Record<string, 'pending' | 'uploading' | 'success' | 'error'>;
}

export interface ChatInputForm {
  message: string;
  mentionedAgent?: string;
  attachments: File[];
}

// Theme and styling types
export interface ThemeColors {
  primary: string;
  secondary: string;
  success: string;
  warning: string;
  error: string;
}

export interface AgentAvatarConfig {
  bgColor: string;
  color?: string;
  imgUrl?: string;
}
