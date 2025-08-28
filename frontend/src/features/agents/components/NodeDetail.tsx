import { LoadingSpinner } from '@/shared/components/LoadingSpinner';
import { useAppStore } from '@/shared/stores/appStore';
import type { ExecutionNode } from '@/shared/types';
import { useNavigate, useParams } from '@modern-js/runtime/router';
import type { FC } from 'react';
import { useEffect, useState } from 'react';

const NodeDetail: FC = () => {
  const { nodeId } = useParams<{ nodeId: string }>();
  const navigate = useNavigate();
  const [nodeData, setNodeData] = useState<ExecutionNode | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { setCurrentView, setSelectedNode } = useAppStore();

  useEffect(() => {
    setCurrentView('node-detail');
    setSelectedNode(nodeId || null);

    return () => {
      setCurrentView('dashboard');
      setSelectedNode(null);
    };
  }, [nodeId, setCurrentView, setSelectedNode]);

  // Simulate node data fetching
  useEffect(() => {
    if (!nodeId) {
      setError('No node ID provided');
      setIsLoading(false);
      return;
    }

    const fetchNodeData = async () => {
      try {
        setIsLoading(true);
        // This would normally be an API call
        // const response = await fetch(`/api/node/${nodeId}`);
        // const data = await response.json();

        // Mock data for demonstration
        const mockNode: ExecutionNode = {
          node_id: nodeId,
          caller: 'user',
          callee: 'master_agent',
          node_type: 'agent',
          status: 'completed',
          trace_id: 'trace_123',
          create_time: new Date().toISOString(),
          input: {
            class_attr: {
              temperature: 0.7,
              max_tokens: 1000,
              stream: false,
            },
            arguments: {
              query: 'Hello, how can you help me?',
              messages: [{ role: 'user', content: 'Hello, how can you help me?' }],
            },
          },
          output:
            'I can help you with various tasks including answering questions, providing information, and assisting with problem-solving.',
          pre_id: '',
          next_id: '',
        };

        setTimeout(() => {
          setNodeData(mockNode);
          setIsLoading(false);
        }, 1000);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load node data');
        setIsLoading(false);
      }
    };

    fetchNodeData();
  }, [nodeId]);

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleRegenerate = async () => {
    if (!nodeData) return;

    try {
      setIsLoading(true);
      // This would trigger a regeneration API call
      // await fetch('/api/regenerate', { method: 'POST', body: JSON.stringify(nodeData.input) });

      // Mock regeneration
      setTimeout(() => {
        setNodeData((prev) =>
          prev
            ? {
                ...prev,
                output:
                  'Regenerated response: I can assist you with a wide variety of tasks and questions. How may I help you today?',
                status: 'completed',
              }
            : null
        );
        setIsLoading(false);
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to regenerate');
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading node details..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <svg
            className="w-16 h-16 mx-auto mb-4 text-red-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Node</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button type="button" onClick={handleBack} className="btn btn-primary">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (!nodeData) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Node Not Found</h2>
          <p className="text-gray-600 mb-4">The requested node could not be found.</p>
          <button type="button" onClick={handleBack} className="btn btn-primary">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button type="button" onClick={handleBack} className="btn btn-ghost btn-sm">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              Back
            </button>
            <h1 className="text-xl font-bold text-gray-900">Node Detail</h1>
            <span className="text-sm text-gray-500">ID: {nodeData.node_id}</span>
          </div>

          <div className="flex items-center space-x-2">
            <span
              className={`status-indicator ${
                nodeData.status === 'completed'
                  ? 'status-success'
                  : nodeData.status === 'error'
                    ? 'status-error'
                    : nodeData.status === 'running'
                      ? 'status-working'
                      : 'status-idle'
              }`}
            >
              {nodeData.status}
            </span>

            {nodeData.node_type === 'llm' && (
              <button
                type="button"
                onClick={handleRegenerate}
                className="btn btn-secondary btn-sm"
                disabled={isLoading}
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Regenerate
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
          {/* Configuration Panel */}
          <div className="card">
            <div className="card-header">
              <h2 className="text-lg font-semibold">Configuration</h2>
            </div>
            <div className="card-content overflow-y-auto">
              {/* Basic Info */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Basic Information
                  </label>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Caller:</span>
                      <span className="ml-2 font-medium">{nodeData.caller}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Callee:</span>
                      <span className="ml-2 font-medium">{nodeData.callee}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Type:</span>
                      <span className="ml-2 font-medium">{nodeData.node_type}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Trace ID:</span>
                      <span className="ml-2 font-mono text-xs">{nodeData.trace_id}</span>
                    </div>
                  </div>
                </div>

                {/* Class Attributes */}
                {nodeData.input.class_attr && Object.keys(nodeData.input.class_attr).length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Class Attributes
                    </label>
                    <div className="space-y-2">
                      {Object.entries(nodeData.input.class_attr).map(([key, value]) => (
                        <div key={key} className="flex items-center space-x-2">
                          <label className="text-sm text-gray-600 w-24">{key}:</label>
                          <input
                            type="text"
                            value={String(value)}
                            readOnly
                            className="input text-sm flex-1"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Arguments */}
                {nodeData.input.arguments && Object.keys(nodeData.input.arguments).length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Arguments
                    </label>
                    <div className="space-y-2">
                      {Object.entries(nodeData.input.arguments).map(([key, value]) => (
                        <div key={key}>
                          <label className="block text-sm text-gray-600 mb-1">{key}:</label>
                          {Array.isArray(value) ? (
                            <div className="space-y-1">
                              {value.map((item, idx) => (
                                <div key={idx} className="bg-gray-50 p-2 rounded text-sm">
                                  {typeof item === 'object' ? (
                                    <pre className="whitespace-pre-wrap">
                                      {JSON.stringify(item, null, 2)}
                                    </pre>
                                  ) : (
                                    String(item)
                                  )}
                                </div>
                              ))}
                            </div>
                          ) : (
                            <textarea
                              value={
                                typeof value === 'object'
                                  ? JSON.stringify(value, null, 2)
                                  : String(value)
                              }
                              readOnly
                              rows={3}
                              className="input text-sm w-full resize-none"
                            />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Output Panel */}
          <div className="card">
            <div className="card-header">
              <h2 className="text-lg font-semibold">Output</h2>
            </div>
            <div className="card-content overflow-y-auto">
              {nodeData.output ? (
                <div className="prose prose-sm max-w-none">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 bg-gray-50 p-4 rounded">
                    {nodeData.output}
                  </pre>
                </div>
              ) : (
                <div className="flex items-center justify-center h-32 text-gray-500">
                  <div className="text-center">
                    <svg
                      className="w-12 h-12 mx-auto mb-2 text-gray-300"
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
                    <p>No output available</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NodeDetail;
