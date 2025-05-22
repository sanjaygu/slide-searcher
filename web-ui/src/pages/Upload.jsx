import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation } from 'react-query';
import axios from 'axios';

const Upload = () => {
  const uploadMutation = useMutation((files) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });
    return axios.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  });

  const onDrop = useCallback((acceptedFiles) => {
    uploadMutation.mutate(acceptedFiles);
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/pdf': ['.pdf'],
    },
  });

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Upload Presentation Slides
        </h1>
        <p className="text-gray-600 mb-8">
          Upload PPTX or PDF files to make them searchable
        </p>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
            ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'}`}
        >
          <input {...getInputProps()} />
          {uploadMutation.isLoading ? (
            <p className="text-gray-600">Uploading...</p>
          ) : isDragActive ? (
            <p className="text-primary-600">Drop the files here...</p>
          ) : (
            <div>
              <p className="text-gray-600">
                Drag and drop files here, or click to select files
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Supported formats: PPTX, PDF
              </p>
            </div>
          )}
        </div>

        {uploadMutation.isSuccess && (
          <div className="mt-4 text-green-600">
            Files uploaded successfully!
          </div>
        )}

        {uploadMutation.isError && (
          <div className="mt-4 text-red-600">
            Error uploading files. Please try again.
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload; 