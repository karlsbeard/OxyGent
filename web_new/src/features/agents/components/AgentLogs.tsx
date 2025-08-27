import { useAppStore } from '@/shared/stores/appStore';
import { clsx } from 'clsx';
import { format } from 'date-fns';
import type { FC } from 'react';
import { useEffect, useRef, useState } from 'react';

interface LogEntry {
  id: string;
  timestamp: Date;
  level: 'info' | 'warning' | 'error' | 'debug';
  agentId: string;
  message: string;
  details?: string;
}

export const AgentLogs: FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filterLevel, setFilterLevel] = useState<string>('all');
  const [filterAgent, setFilterAgent] = useState<string>('all');
  const [isAutoScroll, setIsAutoScroll] = useState(true);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const logsContainerRef = useRef<HTMLDivElement>(null);

  const { agents, messages, executionHistory } = useAppStore();

  // Mock log generation from messages and execution history
  useEffect(() => {
    const newLogs: LogEntry[] = [];

    // Convert messages to log entries
    messages.forEach((message) => {
      if (message.agentId) {
        newLogs.push({
          id: `msg-${message.id}`,
          timestamp: message.timestamp,
          level: 'info',
          agentId: message.agentId,
          message: `Message: ${message.content.slice(0, 50)}${message.content.length > 50 ? '...' : ''}`,
          details: message.content,
        });
      }
    });

    // Convert agent status changes to logs
    agents.forEach((agent) => {
      if (agent.status === 'working' || agent.status === 'error') {
        newLogs.push({
          id: `agent-${agent.id}-${Date.now()}`,
          timestamp: new Date(),
          level: agent.status === 'error' ? 'error' : 'info',
          agentId: agent.name,
          message: `Agent status: ${agent.status}`,
          details: agent.description || undefined,
        });
      }
    });

    // Sort logs by timestamp (newest first)
    newLogs.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());

    setLogs(newLogs.slice(0, 100)); // Keep only last 100 logs
  }, [messages, agents, executionHistory]);

  // Auto scroll to bottom when new logs arrive
  useEffect(() => {
    if (isAutoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, isAutoScroll]);

  // Handle manual scroll detection
  const handleScroll = () => {
    if (!logsContainerRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = logsContainerRef.current;
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;

    setIsAutoScroll(isNearBottom);
  };

  const filteredLogs = logs.filter((log) => {
    const levelMatch = filterLevel === 'all' || log.level === filterLevel;
    const agentMatch = filterAgent === 'all' || log.agentId === filterAgent;
    return levelMatch && agentMatch;
  });

  const uniqueAgents = Array.from(new Set(logs.map((log) => log.agentId))).sort();

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'debug':
        return 'text-gray-600 bg-gray-50 border-gray-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'error':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        );
      case 'warning':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        );
      case 'debug':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        );
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Filters */}
      <div className="flex items-center space-x-4 p-2 border-b border-gray-200 bg-gray-50 rounded-t-lg">
        <div className="flex items-center space-x-2">
          <label htmlFor="level-filter" className="text-xs font-medium text-gray-700">
            Level:
          </label>
          <select
            id="level-filter"
            value={filterLevel}
            onChange={(e) => setFilterLevel(e.target.value)}
            className="text-xs border border-gray-300 rounded px-2 py-1 bg-white"
          >
            <option value="all">All</option>
            <option value="error">Error</option>
            <option value="warning">Warning</option>
            <option value="info">Info</option>
            <option value="debug">Debug</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <label htmlFor="agent-filter" className="text-xs font-medium text-gray-700">
            Agent:
          </label>
          <select
            id="agent-filter"
            value={filterAgent}
            onChange={(e) => setFilterAgent(e.target.value)}
            className="text-xs border border-gray-300 rounded px-2 py-1 bg-white"
          >
            <option value="all">All</option>
            {uniqueAgents.map((agent) => (
              <option key={agent} value={agent}>
                {agent}
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1" />

        <button
          type="button"
          onClick={() => setLogs([])}
          className="text-xs text-gray-600 hover:text-gray-800 px-2 py-1 rounded hover:bg-gray-100"
          title="Clear logs"
        >
          Clear
        </button>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="auto-scroll"
            checked={isAutoScroll}
            onChange={(e) => setIsAutoScroll(e.target.checked)}
            className="text-xs"
          />
          <label htmlFor="auto-scroll" className="text-xs text-gray-700">
            Auto-scroll
          </label>
        </div>
      </div>

      {/* Logs */}
      <div
        ref={logsContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto p-2 space-y-2 bg-gray-900 text-gray-100 font-mono text-sm"
      >
        {filteredLogs.length === 0 ? (
          <div className="flex items-center justify-center h-32 text-gray-400">
            <div className="text-center">
              <svg
                className="w-8 h-8 mx-auto mb-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <p>No logs to display</p>
            </div>
          </div>
        ) : (
          filteredLogs.map((log) => (
            <div
              key={log.id}
              className={clsx('flex items-start space-x-3 p-2 rounded border-l-4', {
                'border-red-500 bg-red-900/10': log.level === 'error',
                'border-yellow-500 bg-yellow-900/10': log.level === 'warning',
                'border-blue-500 bg-blue-900/10': log.level === 'info',
                'border-gray-500 bg-gray-800/50': log.level === 'debug',
              })}
            >
              {/* Level Icon */}
              <div
                className={clsx('flex-shrink-0 mt-0.5', {
                  'text-red-400': log.level === 'error',
                  'text-yellow-400': log.level === 'warning',
                  'text-blue-400': log.level === 'info',
                  'text-gray-400': log.level === 'debug',
                })}
              >
                {getLevelIcon(log.level)}
              </div>

              {/* Log Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-xs text-gray-400">
                    {format(log.timestamp, 'HH:mm:ss.SSS')}
                  </span>
                  <span
                    className={clsx('text-xs px-1 py-0.5 rounded uppercase font-semibold', {
                      'bg-red-900 text-red-200': log.level === 'error',
                      'bg-yellow-900 text-yellow-200': log.level === 'warning',
                      'bg-blue-900 text-blue-200': log.level === 'info',
                      'bg-gray-800 text-gray-300': log.level === 'debug',
                    })}
                  >
                    {log.level}
                  </span>
                  <span className="text-xs text-gray-300 font-medium">{log.agentId}</span>
                </div>

                <div className="text-sm text-gray-100">{log.message}</div>

                {log.details && (
                  <details className="mt-1">
                    <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-300">
                      Details
                    </summary>
                    <pre className="text-xs text-gray-300 mt-1 whitespace-pre-wrap break-words bg-gray-800 p-2 rounded">
                      {log.details}
                    </pre>
                  </details>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={logsEndRef} />
      </div>
    </div>
  );
};
