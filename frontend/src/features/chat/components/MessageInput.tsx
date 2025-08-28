import { clsx } from 'clsx';
import type { FC } from 'react';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onKeyPress?: (e: React.KeyboardEvent) => void;
  onFileUpload?: (files: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageInput: FC<MessageInputProps> = ({
  value,
  onChange,
  onKeyPress,
  onFileUpload,
  disabled = false,
  placeholder = 'Type your message...',
}) => {
  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length > 0 && onFileUpload) {
      onFileUpload(files);
    }
    // Reset input to allow selecting same file again
    e.target.value = '';
  };

  return (
    <div className="relative">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={onKeyPress}
        disabled={disabled}
        placeholder={placeholder}
        rows={1}
        className={clsx(
          'input resize-none pr-12 min-h-[36px] max-h-32',
          'focus:ring-1 focus:ring-primary-500 focus:border-primary-500',
          {
            'opacity-50 cursor-not-allowed': disabled,
          }
        )}
        style={{
          height: 'auto',
          minHeight: '36px',
        }}
        onInput={(e) => {
          // Auto-resize textarea
          const target = e.target as HTMLTextAreaElement;
          target.style.height = 'auto';
          target.style.height = `${Math.min(target.scrollHeight, 128)}px`;
        }}
      />

      {/* File Upload Button */}
      <div className="absolute right-2 bottom-2">
        <label
          htmlFor="file-upload"
          className={clsx('cursor-pointer p-1 rounded hover:bg-gray-100 transition-colors', {
            'opacity-50 cursor-not-allowed pointer-events-none': disabled,
          })}
          title="Attach files"
        >
          <input
            id="file-upload"
            type="file"
            multiple
            accept=".txt,.jpg,.jpeg,.png,.mp4,.xlsx,.xls,.doc,.docx,.pdf,.csv,.tsv,.ods,.py,.md,.json"
            onChange={handleFileInputChange}
            disabled={disabled}
            className="hidden"
          />
          <svg
            className="w-5 h-5 text-gray-400 hover:text-gray-600"
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
        </label>
      </div>
    </div>
  );
};
