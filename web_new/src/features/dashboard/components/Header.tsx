import { useSocket } from '@/shared/providers/SocketProvider';
import { useAppStore } from '@/shared/stores/appStore';
import type { FC } from 'react';

export const Header: FC = () => {
  const { isConnected, connectionError, currentScript, masterAgentName } = useAppStore();

  const { connect, disconnect } = useSocket();

  const handleConnectionToggle = () => {
    if (isConnected) {
      disconnect();
    } else {
      connect();
    }
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left side - Logo and title */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <img
              src="/favicon.ico"
              alt="OxyGent"
              className="w-8 h-8"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
              }}
            />
            <h1 className="text-xl font-bold text-gray-900">OxyGent</h1>
          </div>

          {currentScript && (
            <div className="flex items-center space-x-2 px-3 py-1 bg-gray-100 rounded-full">
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
              <span className="text-sm font-medium text-gray-700">{currentScript}</span>
            </div>
          )}
        </div>

        {/* Center - Master agent info */}
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500">Master Agent:</span>
          <span className="font-medium text-gray-900">{masterAgentName}</span>
        </div>

        {/* Right side - Connection status and controls */}
        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            <div
              className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}
            />
            <span
              className={`text-sm font-medium ${isConnected ? 'text-green-700' : 'text-red-700'}`}
            >
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Connection Error */}
          {connectionError && (
            <div className="flex items-center space-x-1 text-red-600" title={connectionError}>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
              <span className="text-xs">Error</span>
            </div>
          )}

          {/* Connection Toggle Button */}
          <button
            type="button"
            onClick={handleConnectionToggle}
            className={`btn btn-sm ${isConnected ? 'btn-secondary' : 'btn-primary'}`}
            title={isConnected ? 'Disconnect' : 'Reconnect'}
          >
            {isConnected ? (
              <>
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
                Disconnect
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Reconnect
              </>
            )}
          </button>

          {/* Settings Button */}
          <button type="button" className="btn btn-ghost btn-sm" title="Settings">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
};
