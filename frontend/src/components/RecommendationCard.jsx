import React from 'react';

const getRankBadgeClass = (rank) => {
  switch(rank) {
    case 1: return 'metallic-gold';
    case 2: return 'metallic-silver';
    case 3: return 'metallic-bronze';
    default: return 'bg-surface-dim text-on-surface';
  }
};

export default function RecommendationCard({ restaurant }) {
  const badgeClass = getRankBadgeClass(restaurant.rank);

  return (
    <div className="bg-surface rounded-2xl p-6 card-shadow border border-surface-dim transition-all duration-300 flex flex-col gap-4 relative">
      <div className={`absolute -left-3 -top-3 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg shadow-md border-2 border-white z-10 ${badgeClass}`}>
        {restaurant.rank}
      </div>
      
      <div className="flex-grow flex flex-col justify-between ml-2">
        <div>
          <div className="flex justify-between items-start mb-1">
            <h3 className="text-headline-md font-headline-md text-on-surface">{restaurant.name}</h3>
            <div className="flex items-center gap-1 bg-surface-container-high px-2 py-1 rounded text-label-sm font-label-sm font-bold">
              <span className="text-zomato-red material-symbols-outlined text-[16px]">star</span> {restaurant.rating}
            </div>
          </div>
          <p className="text-body-md font-body-md text-on-surface-variant mb-2">{restaurant.cuisine}</p>
          <p className="text-label-md font-label-md text-on-surface-variant mb-4">{restaurant.cost}</p>
        </div>
        
        <div className="bg-[#F8F8F8] p-3 rounded-lg flex items-start gap-2 border border-surface-dim">
          <span className="material-symbols-outlined text-zomato-red text-[20px] mt-0.5">insights</span>
          <p className="text-label-sm font-label-sm text-on-surface text-sm">
            <span className="font-bold">AI Pick: </span> {restaurant.explanation}
          </p>
        </div>
      </div>
    </div>
  );
}
