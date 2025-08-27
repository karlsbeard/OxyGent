import { clsx } from 'clsx';
import type { FC } from 'react';
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  onFilesUpload: (files: File[]) => void;
  maxFiles?: number;
  maxSize?: number;
  className?: string;
}

const ALLOWED_TYPES = {
  'text/*': ['.txt', '.md', '.json'],
  'image/*': ['.png', '.jpg', '.jpeg'],
  'application/pdf': ['.pdf'],
  'application/vnd.ms-excel': ['.xls'],
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  'application/msword': ['.doc'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'text/csv': ['.csv'],
  'text/tab-separated-values': ['.tsv'],
  'application/vnd.oasis.opendocument.spreadsheet': ['.ods'],
  'text/x-python': ['.py'],
  'video/mp4': ['.mp4'],
};

export const FileUpload: FC<FileUploadProps> = ({
  onFilesUpload,
  maxFiles = 10,
  maxSize = 10 * 1024 * 1024, // 10MB
  className,
}) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFilesUpload(acceptedFiles);
      }
    },
    [onFilesUpload]
  );

  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject, fileRejections } =
    useDropzone({
      onDrop,
      accept: ALLOWED_TYPES,
      maxFiles,
      maxSize,
    });

  return (
    <div className={clsx('w-full', className)}>
      <div
        {...getRootProps()}
        className={clsx(
          'border-2 border-dashed rounded-lg p-6 cursor-pointer transition-colors',
          'hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500',
          {
            'drag-active': isDragActive,
            'drag-accept': isDragAccept,
            'drag-reject': isDragReject,
            'border-gray-300': !isDragActive,
          }
        )}
      >
        <input {...getInputProps()} />

        <div className="text-center">
          <svg
            className={clsx('mx-auto h-12 w-12 mb-4', {
              'text-gray-400': !isDragActive,
              'text-primary-500': isDragAccept,
              'text-red-500': isDragReject,
            })}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>

          {isDragActive ? (
            <p className="text-lg font-medium">
              {isDragAccept ? (
                <span className="text-primary-600">Drop files here...</span>
              ) : (
                <span className="text-red-600">Some files are not supported</span>
              )}
            </p>
          ) : (
            <>
              <p className="text-lg font-medium text-gray-700">
                Drag & drop files here, or{' '}
                <span className="text-primary-600 underline">browse</span>
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Max {maxFiles} files, {Math.round(maxSize / (1024 * 1024))}MB each
              </p>
              <p className="text-xs text-gray-400 mt-1">
                Supports: Images, documents, videos, code files
              </p>
            </>
          )}
        </div>
      </div>

      {/* File Rejection Errors */}
      {fileRejections.length > 0 && (
        <div className="mt-2 space-y-1">
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name} className="text-sm text-red-600">
              <span className="font-medium">{file.name}</span>:
              {errors.map((error) => (
                <span key={error.code} className="ml-1">
                  {error.message}
                </span>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
