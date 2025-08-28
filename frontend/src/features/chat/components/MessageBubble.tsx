import type { Message } from '@/shared/types';
import { clsx } from 'clsx';
import { format } from 'date-fns';
import type { FC } from 'react';

interface MessageBubbleProps {
  message: Message;
  agentIdDict: Record<string, number>;
  onMentionAgent?: (agentName: string) => void;
}

// Agent avatar configurations (from legacy code)
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

export const MessageBubble: FC<MessageBubbleProps> = ({ message, agentIdDict, onMentionAgent }) => {
  const isUser = message.role === 'user';
  const agentIdx =
    message.agentId && agentIdDict[message.agentId] ? agentIdDict[message.agentId] % 16 : 0;
  const agentAvatar = agentImgMap[agentIdx];

  const handleMentionClick = (agentName: string) => {
    onMentionAgent?.(agentName);
  };

  const renderMessageContent = () => {
    // Handle @mentions in message content
    if (message.at) {
      return (
        <span>
          <button
            type="button"
            onClick={() => handleMentionClick(message.at!)}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            @{message.at}
          </button>{' '}
          {message.content}
        </span>
      );
    }

    return message.content;
  };

  return (
    <div
      className={clsx('flex items-start space-x-3', {
        'flex-row-reverse space-x-reverse': isUser,
      })}
    >
      {/* Avatar */}
      {!isUser && message.agentId && (
        <div
          className="agent-avatar flex-shrink-0"
          style={{ backgroundColor: agentAvatar.bgColor }}
          title={message.agentId}
        >
          <img
            src={agentAvatar.imgUrl}
            alt={message.agentId}
            className="w-full h-full rounded-full object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
              // Show initials instead
              target.parentElement!.textContent = message.agentId!.slice(0, 2).toUpperCase();
            }}
          />
        </div>
      )}

      {isUser && (
        <div className="agent-avatar flex-shrink-0 bg-primary-600 text-white">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            />
          </svg>
        </div>
      )}

      {/* Message Content */}
      <div
        className={clsx('flex flex-col max-w-xs lg:max-w-md', {
          'items-end': isUser,
          'items-start': !isUser,
        })}
      >
        {/* Agent Name */}
        {!isUser && message.agentId && (
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-sm font-medium text-gray-700">{message.agentId}</span>
            <span className="text-xs text-gray-500">{format(message.timestamp, 'HH:mm')}</span>
          </div>
        )}

        {/* Message Bubble */}
        <div
          className={clsx('message-bubble break-words', {
            'message-user': isUser,
            'message-agent': !isUser,
          })}
        >
          <div className="whitespace-pre-wrap">{renderMessageContent()}</div>

          {/* Attachments */}
          {message.attachments && message.attachments.length > 0 && (
            <div className="mt-2 space-y-1">
              {message.attachments.map((attachment, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-2 text-xs bg-gray-100 rounded px-2 py-1"
                >
                  <svg
                    className="w-3 h-3 text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                    />
                  </svg>
                  <span className="font-medium text-gray-700">{attachment.name}</span>
                  <span className="text-gray-500">({Math.round(attachment.size / 1024)}KB)</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Timestamp for user messages */}
        {isUser && (
          <span className="text-xs text-gray-500 mt-1">{format(message.timestamp, 'HH:mm')}</span>
        )}
      </div>
    </div>
  );
};
