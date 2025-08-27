import type { FC } from 'react';
import { useEffect, useState } from 'react';
import { type Layout, Responsive as ResponsiveGridLayout } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { AgentLogs } from '@/features/agents/components/AgentLogs';
import { AgentTree } from '@/features/agents/components/AgentTree';
import { ChatInterface } from '@/features/chat/components/ChatInterface';
import { LoadingSpinner } from '@/shared/components/LoadingSpinner';
import { useAppStore } from '@/shared/stores/appStore';
import { Header } from './Header';

const defaultLayouts: Layout[] = [
  { i: 'chat', x: 0, y: 0, w: 6, h: 12, minW: 4, minH: 8 },
  { i: 'agents', x: 6, y: 0, w: 6, h: 8, minW: 4, minH: 6 },
  { i: 'logs', x: 6, y: 8, w: 6, h: 4, minW: 4, minH: 3 },
];

const Dashboard: FC = () => {
  const [layouts, setLayouts] = useState<Layout[]>(defaultLayouts);
  const { isLoading, agents, messages, rightPanelVisible, toggleRightPanel } = useAppStore();

  // Initialize data on mount
  useEffect(() => {
    // This would typically fetch initial data
    // For now, we'll just set loading to false after a brief delay
    const timer = setTimeout(() => {
      // setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleLayoutChange = (newLayouts: Layout[]) => {
    setLayouts(newLayouts);
    // Persist layout to localStorage
    localStorage.setItem('dashboard-layout', JSON.stringify(newLayouts));
  };

  // Load saved layout on mount
  useEffect(() => {
    const savedLayout = localStorage.getItem('dashboard-layout');
    if (savedLayout) {
      try {
        setLayouts(JSON.parse(savedLayout));
      } catch (error) {
        console.error('Failed to parse saved layout:', error);
      }
    }
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner size="lg" text="Loading OxyGent Dashboard..." />
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header />

      <div className="flex-1 p-4 overflow-hidden">
        <ResponsiveGridLayout
          className="layout"
          layouts={{ lg: layouts }}
          onLayoutChange={(layout: Layout[]) => handleLayoutChange(layout)}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={40}
          isDraggable={true}
          isResizable={true}
          margin={[16, 16]}
          containerPadding={[0, 0]}
        >
          {/* Chat Interface Panel */}
          <div key="chat" className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Chat Interface</h3>
                <div className="flex items-center space-x-2">
                  <span className="status-indicator status-idle">{messages.length} messages</span>
                  <button
                    type="button"
                    onClick={toggleRightPanel}
                    className="btn btn-ghost btn-sm"
                    title={rightPanelVisible ? 'Hide details' : 'Show details'}
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div className="card-content h-full">
              <ChatInterface />
            </div>
          </div>

          {/* Agent Visualization Panel */}
          <div key="agents" className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Agent Network</h3>
                <span className="status-indicator status-working">{agents.length} agents</span>
              </div>
            </div>
            <div className="card-content h-full overflow-hidden">
              <AgentTree />
            </div>
          </div>

          {/* Agent Logs Panel */}
          <div key="logs" className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold">Agent Logs</h3>
            </div>
            <div className="card-content h-full overflow-hidden">
              <AgentLogs />
            </div>
          </div>
        </ResponsiveGridLayout>
      </div>
    </div>
  );
};

export default Dashboard;
