import React from 'react';

interface SkeletonProps {
  className?: string;
  count?: number;
}

const Skeleton: React.FC<SkeletonProps> = ({ className = '', count = 1 }) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <div 
      key={index}
      className={`animate-pulse bg-gray-200 rounded ${className}`}
    />
  ));

  return <>{skeletons}</>;
};

// Specific skeleton variants
export const TaskSkeleton: React.FC<{ count?: number }> = ({ count = 1 }) => {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, index) => (
        <div 
          key={index} 
          className="rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md shadow-glass p-6 animate-pulse"
        >
          <div className="h-6 bg-gray-300 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-300 rounded w-full mb-2"></div>
          <div className="h-4 bg-gray-300 rounded w-2/3 mb-4"></div>
          <div className="flex space-x-2">
            <div className="h-3 w-3 rounded-full bg-gray-300"></div>
            <div className="h-3 w-3 rounded-full bg-gray-300"></div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Skeleton;