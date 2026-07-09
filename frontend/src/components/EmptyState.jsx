import React from 'react';

export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center h-full">
      <span className="material-symbols-outlined text-6xl text-surface-dim mb-4">travel_explore</span>
      <h3 className="text-headline-md font-headline-md text-on-surface mb-2">Your top picks will appear here</h3>
      <p className="text-body-md font-body-md text-on-surface-variant max-w-sm">
        Adjust your preferences on the left and click 'Get Recommendations' to discover your next great meal.
      </p>
    </div>
  );
}
