import { useSocket } from '@/shared/providers/SocketProvider';
import { useAppStore } from '@/shared/stores/appStore';
import type { Message } from '@/shared/types';
import type { FC } from 'react';
import { useEffect, useRef, useState } from 'react';
import { FileUpload } from './FileUpload';
import { MessageInput } from './MessageInput';
import { MessageList } from './MessageList';

export const ChatInterface: FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [mentionedAgent, setMentionedAgent] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, isConnected, addMessage, masterAgentName, agentIdDict } = useAppStore();

  const { sendMessage: socketSendMessage } = useSocket();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() && selectedFiles.length === 0) return;
    if (!isConnected) {
      console.warn('Not connected to server');
      return;
    }

    // Create user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
      attachments: selectedFiles.map((file) => ({
        name: file.name,
        size: file.size,
        type: file.type,
      })),
      at: mentionedAgent || undefined,
    };

    // Add to local state immediately for optimistic update
    addMessage(userMessage);

    // Prepare payload for server
    const payload = {
      from_trace_id: '', // Will be managed by server
      query: inputMessage,
      shared_data: { extra: 'extra argument' },
      attachments: selectedFiles.map((file) => file.name),
      callee: mentionedAgent || undefined,
    };

    try {
      // Send via WebSocket
      socketSendMessage(payload);

      // Clear input
      setInputMessage('');
      setSelectedFiles([]);
      setMentionedAgent('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileUpload = (files: File[]) => {
    setSelectedFiles((prev) => [...prev, ...files]);
  };

  const handleFileRemove = (fileName: string) => {
    setSelectedFiles((prev) => prev.filter((file) => file.name !== fileName));
  };

  const handleMentionAgent = (agentName: string) => {
    setMentionedAgent(agentName);
  };

  const clearMentionedAgent = () => {
    setMentionedAgent('');
  };

  // Initialize with welcome message if no messages
  useEffect(() => {
    if (messages.length === 0 && masterAgentName) {
      const welcomeMessage: Message = {
        id: 'welcome',
        role: 'agent',
        content: 'Hello! How may I assist you today?',
        timestamp: new Date(),
        agentId: masterAgentName,
      };
      addMessage(welcomeMessage);
    }
  }, [messages.length, masterAgentName, addMessage]);

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <MessageList
          messages={messages}
          agentIdDict={agentIdDict}
          onMentionAgent={handleMentionAgent}
        />
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 space-y-3">
        {/* File Upload Preview */}
        {selectedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {selectedFiles.map((file) => (
              <div
                key={file.name}
                className="flex items-center space-x-2 bg-gray-100 rounded-lg px-3 py-2"
              >
                <svg
                  className="w-4 h-4 text-gray-500"
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
                <span className="text-sm font-medium text-gray-700">{file.name}</span>
                <button
                  type="button"
                  onClick={() => handleFileRemove(file.name)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Mentioned Agent */}
        {mentionedAgent && (
          <div className="flex items-center space-x-2 bg-blue-50 rounded-lg px-3 py-2">
            <span className="text-sm text-blue-700">
              Mentioning: <span className="font-medium">@{mentionedAgent}</span>
            </span>
            <button
              type="button"
              onClick={clearMentionedAgent}
              className="text-blue-400 hover:text-blue-600"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        )}

        {/* Message Input */}
        <div className="flex items-end space-x-2">
          <div className="flex-1">
            <MessageInput
              value={inputMessage}
              onChange={setInputMessage}
              onKeyPress={handleKeyPress}
              onFileUpload={handleFileUpload}
              disabled={!isConnected}
              placeholder={isConnected ? 'Ask me anything here...' : 'Connecting to server...'}
            />
          </div>

          <button
            type="button"
            onClick={handleSendMessage}
            disabled={!isConnected || (!inputMessage.trim() && selectedFiles.length === 0)}
            className="btn btn-primary btn-md flex-shrink-0"
            title="Send message"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </div>

        {/* Connection Status */}
        {!isConnected && (
          <div className="text-center py-2">
            <span className="text-sm text-red-600 flex items-center justify-center space-x-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
              <span>Disconnected from server</span>
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
