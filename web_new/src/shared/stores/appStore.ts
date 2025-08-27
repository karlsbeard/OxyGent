import type {
  Agent,
  ChatHistory,
  ConnectionState,
  ExecutionNode,
  LayoutState,
  Message,
} from '@/shared/types';
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface AppState extends ConnectionState, LayoutState {
  // Data state
  messages: Message[];
  agents: Agent[];
  executionHistory: ChatHistory[];
  currentScript: string;
  agentIdDict: Record<string, number>;
  masterAgentName: string;

  // Loading states
  isLoading: boolean;
  isLoadingAgents: boolean;
  isLoadingMessages: boolean;

  // Actions - Connection
  setConnection: (connected: boolean, error?: string) => void;
  incrementReconnectAttempts: () => void;
  resetReconnectAttempts: () => void;

  // Actions - UI State
  toggleSidebar: () => void;
  toggleRightPanel: () => void;
  setCurrentView: (view: LayoutState['currentView']) => void;
  setSelectedNode: (nodeId: string | null) => void;

  // Actions - Data
  addMessage: (message: Message) => void;
  updateMessage: (messageId: string, updates: Partial<Message>) => void;
  clearMessages: () => void;

  updateAgent: (agent: Agent) => void;
  setAgents: (agents: Agent[]) => void;

  addExecutionStep: (step: ChatHistory) => void;
  setExecutionHistory: (history: ChatHistory[]) => void;
  clearExecutionHistory: () => void;

  setAgentIdDict: (dict: Record<string, number>) => void;
  setMasterAgentName: (name: string) => void;
  setCurrentScript: (script: string) => void;

  // Actions - Loading states
  setLoading: (loading: boolean) => void;
  setLoadingAgents: (loading: boolean) => void;
  setLoadingMessages: (loading: boolean) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    (set, get) => ({
      // Initial state - Connection
      isConnected: false,
      connectionError: null,
      reconnectAttempts: 0,

      // Initial state - Layout
      sidebarCollapsed: false,
      rightPanelVisible: false,
      currentView: 'dashboard',
      selectedNodeId: null,

      // Initial state - Data
      messages: [],
      agents: [],
      executionHistory: [],
      currentScript: '',
      agentIdDict: {},
      masterAgentName: 'master_agent',

      // Initial state - Loading
      isLoading: false,
      isLoadingAgents: false,
      isLoadingMessages: false,

      // Actions - Connection
      setConnection: (connected, error) =>
        set(
          {
            isConnected: connected,
            connectionError: error || null,
            // Reset reconnect attempts on successful connection
            reconnectAttempts: connected ? 0 : get().reconnectAttempts,
          },
          false,
          'setConnection'
        ),

      incrementReconnectAttempts: () =>
        set((state) => ({ reconnectAttempts: state.reconnectAttempts + 1 })),

      resetReconnectAttempts: () => set({ reconnectAttempts: 0 }),

      // Actions - UI State
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      toggleRightPanel: () => set((state) => ({ rightPanelVisible: !state.rightPanelVisible })),

      setCurrentView: (view) => set({ currentView: view }),

      setSelectedNode: (nodeId) => set({ selectedNodeId: nodeId }),

      // Actions - Data
      addMessage: (message) =>
        set(
          (state) => ({
            messages: [...state.messages, message],
          }),
          false,
          'addMessage'
        ),

      updateMessage: (messageId, updates) =>
        set(
          (state) => ({
            messages: state.messages.map((msg) =>
              msg.id === messageId ? { ...msg, ...updates } : msg
            ),
          }),
          false,
          'updateMessage'
        ),

      clearMessages: () => set({ messages: [] }),

      updateAgent: (agent) =>
        set(
          (state) => ({
            agents: state.agents.map((a) => (a.id === agent.id ? { ...a, ...agent } : a)),
          }),
          false,
          'updateAgent'
        ),

      setAgents: (agents) => set({ agents }),

      addExecutionStep: (step) =>
        set(
          (state) => ({
            executionHistory: [...state.executionHistory, step],
          }),
          false,
          'addExecutionStep'
        ),

      setExecutionHistory: (history) => set({ executionHistory: history }),

      clearExecutionHistory: () => set({ executionHistory: [] }),

      setAgentIdDict: (dict) => set({ agentIdDict: dict }),

      setMasterAgentName: (name) => set({ masterAgentName: name }),

      setCurrentScript: (script) => set({ currentScript: script }),

      // Actions - Loading states
      setLoading: (loading) => set({ isLoading: loading }),

      setLoadingAgents: (loading) => set({ isLoadingAgents: loading }),

      setLoadingMessages: (loading) => set({ isLoadingMessages: loading }),
    }),
    {
      name: 'oxygent-app-store',
      // Only include non-sensitive data in devtools
      serialize: {
        options: {
          // Exclude functions and large objects from devtools
          map: {
            messages: (messages: Message[]) => `${messages.length} messages`,
            agents: (agents: Agent[]) => `${agents.length} agents`,
            executionHistory: (history: ChatHistory[]) => `${history.length} steps`,
          },
        },
      },
    }
  )
);
