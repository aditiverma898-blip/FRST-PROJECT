import React from 'react';

export default function LoadingState() {
  return (
    <div className="bg-surface rounded-2xl p-6 border border-surface-dim animate-pulse flex flex-col gap-6">
      <div className="flex-grow flex flex-col justify-between py-2">
        <div>
          <div className="h-6 bg-surface-variant rounded w-1/2 mb-3"></div>
          <div className="h-4 bg-surface-variant rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-surface-variant rounded w-1/4 mb-6"></div>
        </div>
        <div className="h-16 bg-surface-variant rounded w-full flex items-center justify-center">
          <span className="text-on-surface-variant text-label-sm font-label-sm flex items-center gap-2">
            <span className="material-symbols-outlined animate-spin">sync</span>
            AI is ranking restaurants for you...
          </span>
        </div>
      </div>
    </div>
  );
}
