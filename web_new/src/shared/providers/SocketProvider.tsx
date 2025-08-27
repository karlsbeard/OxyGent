import { useAppStore } from '@/shared/stores/appStore';
import type { WebSocketMessage } from '@/shared/types';
import type { FC, ReactNode } from 'react';
import { createContext, useContext, useEffect, useRef, useState } from 'react';
import { type Socket, io } from 'socket.io-client';

interface SocketContextValue {
  socket: Socket | null;
  connect: () => void;
  disconnect: () => void;
  sendMessage: (data: unknown) => void;
}

const SocketContext = createContext<SocketContextValue | null>(null);

interface SocketProviderProps {
  children: ReactNode;
}

export const SocketProvider: FC<SocketProviderProps> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const {
    setConnection,
    addMessage,
    updateAgent,
    addExecutionStep,
    incrementReconnectAttempts,
    resetReconnectAttempts,
    reconnectAttempts,
  } = useAppStore();

  const connect = () => {
    try {
      const newSocket = io('ws://localhost:8000', {
        transports: ['websocket', 'polling'],
        timeout: 20000,
        forceNew: true,
      });

      newSocket.on('connect', () => {
        console.log('Socket connected');
        setConnection(true);
        resetReconnectAttempts();
        newSocket.emit('start');
      });

      newSocket.on('disconnect', (reason) => {
        console.log('Socket disconnected:', reason);
        setConnection(false, reason);

        // Auto-reconnect logic
        if (reconnectAttempts < 5) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
          reconnectTimeoutRef.current = setTimeout(() => {
            incrementReconnectAttempts();
            connect();
          }, delay);
        }
      });

      newSocket.on('connect_error', (error) => {
        console.error('Socket connection error:', error);
        setConnection(false, error.message);
      });

      newSocket.on('message', (data: string) => {
        try {
          if (data.startsWith('服务器')) {
            console.log(data);
            return;
          }

          const message: WebSocketMessage = JSON.parse(data);
          console.log('Received message:', message);

          // Handle different message types
          switch (message.type) {
            case 'tool_call':
              handleToolCall(message);
              break;
            case 'observation':
              handleObservation(message);
              break;
            default:
              console.log('Unknown message type:', message.type);
          }
        } catch (error) {
          console.error('Error parsing socket message:', error);
        }
      });

      setSocket(newSocket);
    } catch (error) {
      console.error('Failed to create socket connection:', error);
      setConnection(false, 'Failed to create connection');
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }

    if (socket) {
      socket.disconnect();
      setSocket(null);
    }

    setConnection(false);
  };

  const sendMessage = (data: unknown) => {
    if (socket?.connected) {
      socket.emit('chat', data);
    } else {
      console.warn('Socket not connected, cannot send message');
    }
  };

  const handleToolCall = (message: WebSocketMessage) => {
    // Handle agent-to-agent communication
    if (
      message.content?.caller_category === 'agent' &&
      message.content?.callee_category === 'agent' &&
      message.content?.arguments
    ) {
      const newMessage = {
        id: crypto.randomUUID(),
        role: 'agent' as const,
        content: (message.content.arguments as { query?: string }).query || '',
        timestamp: new Date(message.timestamp),
        agentId: message.content.callee,
        at: message.content.caller,
      };
      addMessage(newMessage);
    }
  };

  const handleObservation = (message: WebSocketMessage) => {
    if (message.content?.caller === 'user') {
      // Handle user response
      const content =
        typeof message.content.output === 'string'
          ? message.content.output
          : JSON.stringify(message.content.output, null, 2);

      const newMessage = {
        id: crypto.randomUUID(),
        role: 'agent' as const,
        content,
        timestamp: new Date(message.timestamp),
        agentId: message.content.callee,
      };
      addMessage(newMessage);
    }
  };

  // Initialize connection on mount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, []);

  const contextValue: SocketContextValue = {
    socket,
    connect,
    disconnect,
    sendMessage,
  };

  return <SocketContext.Provider value={contextValue}>{children}</SocketContext.Provider>;
};

export const useSocket = (): SocketContextValue => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within SocketProvider');
  }
  return context;
};
