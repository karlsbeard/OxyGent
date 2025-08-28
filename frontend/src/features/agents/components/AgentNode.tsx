import type { Agent } from '@/shared/types';
import { clsx } from 'clsx';
import type { FC } from 'react';

interface AgentNodeProps {
  agent: Agent;
  agentIdDict: Record<string, number>;
  isExpanded: boolean;
  onToggle: () => void;
  level: number;
}

// Agent avatar configurations (matching legacy system)
const agentImgMap = [
  { bgColor: '#FEEAD4', color: '#7d4303', imgUrl: '/image/agents/agent_0.png' },
  { bgColor: '#E4FBCC', color: '#417609', imgUrl: '/image/agents/agent_1.png' },
  { bgColor: '#D3F8DF', color: '#116e30', imgUrl: '/image/agents/agent_2.png' },
  { bgColor: '#E0F2FE', color: '#044c7c', imgUrl: '/image/agents/agent_3.png' },
  { bgColor: '#E0EAFF', color: '#002980', imgUrl: '/image/agents/agent_4.png' },
  { bgColor: '#EFF1F5', color: '#313b4e', imgUrl: '/image/agents/agent_5.png' },
  { bgColor: '#FBE8FF', color: '#690080', imgUrl: '/image/agents/agent_6.png' },
  { bgColor: '#FBE7F6', color: '#6d1257', imgUrl: '/image/agents/agent_7.png' },
  { bgColor: '#FEF7C4', color: '#7d6e02', imgUrl: '/image/agents/agent_8.png' },
  { bgColor: '#E6F4D7', color: '#41641b', imgUrl: '/image/agents/agent_9.png' },
  { bgColor: '#D5F5F6', color: '#166669', imgUrl: '/image/agents/agent_10.png' },
  { bgColor: '#D2E9FF', color: '#004180', imgUrl: '/image/agents/agent_11.png' },
  { bgColor: '#D1DFFF', color: '#002780', imgUrl: '/image/agents/agent_12.png' },
  { bgColor: '#D5D9EB', color: '#293156', imgUrl: '/image/agents/agent_13.png' },
  { bgColor: '#EBE9FE', color: '#11067a', imgUrl: '/image/agents/agent_14.png' },
  { bgColor: '#FFE4E8', color: '#800013', imgUrl: '/image/agents/agent_15.png' },
];

const typeIconMap = {
  tool: (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
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
  ),
  llm: (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
      />
    </svg>
  ),
  flow: (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M13 10V3L4 14h7v7l9-11h-7z"
      />
    </svg>
  ),
};

export const AgentNode: FC<AgentNodeProps> = ({
  agent,
  agentIdDict,
  isExpanded,
  onToggle,
  level,
}) => {
  const isAgent =
    agent.type === 'react' ||
    agent.type === 'chat' ||
    agent.type === 'workflow' ||
    agent.type === 'parallel';
  const agentIdx = agentIdDict[agent.name] ? agentIdDict[agent.name] % 16 : 0;
  const agentAvatar = agentImgMap[agentIdx];
  const hasChildren = agent.children && agent.children.length > 0;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'working':
        return 'border-blue-500 bg-blue-50';
      case 'error':
        return 'border-red-500 bg-red-50';
      case 'completed':
        return 'border-green-500 bg-green-50';
      default:
        return 'border-gray-200 bg-white';
    }
  };

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case 'working':
        return <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />;
      case 'error':
        return <div className="w-2 h-2 bg-red-500 rounded-full" />;
      case 'completed':
        return <div className="w-2 h-2 bg-green-500 rounded-full" />;
      default:
        return <div className="w-2 h-2 bg-gray-300 rounded-full" />;
    }
  };

  return (
    <div className="relative">
      {/* Connection line for non-root nodes */}
      {level > 0 && <div className="absolute -left-4 top-4 w-4 h-0.5 bg-gray-300" />}

      <div
        className={clsx(
          'relative flex items-center p-3 rounded-lg border-2 transition-all cursor-pointer hover:shadow-sm',
          getStatusColor(agent.status),
          {
            'shadow-md': agent.status === 'working',
          }
        )}
        onClick={onToggle}
      >
        {/* Expand/Collapse Button */}
        {hasChildren && (
          <button
            type="button"
            className="absolute -left-2 -top-2 w-4 h-4 bg-white border border-gray-300 rounded-full flex items-center justify-center hover:bg-gray-50 z-10"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <svg
              className={clsx('w-2 h-2 text-gray-600 transition-transform', {
                'rotate-90': isExpanded,
              })}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        )}

        {/* Agent Avatar or Type Icon */}
        <div className="flex-shrink-0 mr-3">
          {isAgent ? (
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
              style={{ backgroundColor: agentAvatar.bgColor, color: agentAvatar.color }}
              title={`Agent: ${agent.name}`}
            >
              <img
                src={agentAvatar.imgUrl}
                alt={agent.name}
                className="w-full h-full rounded-full object-cover"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  // Show initials instead
                  target.parentElement!.textContent = agent.name.slice(0, 2).toUpperCase();
                }}
              />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600">
              {typeIconMap[agent.type as keyof typeof typeIconMap] || typeIconMap.tool}
            </div>
          )}
        </div>

        {/* Agent Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <h4 className="font-medium text-gray-900 truncate">{agent.name}</h4>
            {getStatusIndicator(agent.status)}
            {agent.isRemote && (
              <div className="w-2 h-2 bg-purple-500 rounded-full" title="Remote agent" />
            )}
          </div>

          <div className="flex items-center space-x-2 mt-1">
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
              {agent.type}
            </span>

            {agent.tools && agent.tools.length > 0 && (
              <span className="text-xs text-gray-500" title={agent.tools.join(', ')}>
                {agent.tools.length} tools
              </span>
            )}
          </div>

          {agent.description && (
            <p className="text-xs text-gray-600 mt-1 truncate" title={agent.description}>
              {agent.description}
            </p>
          )}
        </div>

        {/* Status Badge */}
        <div className="flex-shrink-0">
          <span
            className={clsx('status-indicator text-xs', {
              'status-working': agent.status === 'working',
              'status-error': agent.status === 'error',
              'status-success': agent.status === 'completed',
              'status-idle': agent.status === 'idle',
            })}
          >
            {agent.status}
          </span>
        </div>
      </div>
    </div>
  );
};
