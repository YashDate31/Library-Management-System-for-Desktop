import React from 'react';

export default function LoadingSpinner({ size = 'md', className = '' }) {
  const sizeClasses = {
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
    xl: 'w-16 h-16 border-4'
  };

  const currentSize = sizeClasses[size] || sizeClasses.md;

  return (
    <div className={`flex flex-col items-center justify-center gap-2 ${className}`}>
      <div 
        className={`${currentSize} border-slate-200 border-t-blue-500 rounded-full animate-spin`}
        role="status"
        aria-label="Loading"
      />
    </div>
  );
}
