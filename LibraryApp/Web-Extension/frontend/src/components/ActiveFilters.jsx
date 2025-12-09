import React from 'react';
import { X, Filter } from 'lucide-react';

export default function ActiveFilters({ activeFilters, onRemove, onClear }) {
  // activeFilters is an object like: { searchTerm: '...', category: '...', availability: '...' }
  
  // Convert object to array of active filter items for rendering
  const filterParams = [];

  if (activeFilters.searchTerm) {
    filterParams.push({ key: 'searchTerm', label: `Search: "${activeFilters.searchTerm}"` });
  }
  if (activeFilters.category && activeFilters.category !== 'All') {
    filterParams.push({ key: 'category', label: activeFilters.category });
  }
  if (activeFilters.availability && activeFilters.availability !== 'all') {
    const label = activeFilters.availability === 'available' ? 'Available' : 'Out of Stock';
    filterParams.push({ key: 'availability', label: label });
  }

  if (filterParams.length === 0) return null;

  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-3 animate-fade-in-up">
      
      <div className="flex items-center gap-2 text-slate-500 font-bold text-sm uppercase tracking-wide shrink-0">
         <Filter size={14} /> Active Filters:
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {filterParams.map((filter) => (
          <button
            key={filter.key}
            onClick={() => onRemove(filter.key)}
            className="group flex items-center gap-1.5 pl-3 pr-2 py-1.5 bg-blue-50 text-blue-700 text-sm font-semibold rounded-full border border-blue-100 hover:bg-red-50 hover:text-red-600 hover:border-red-100 transition-all"
          >
            {filter.label}
            <div className="p-0.5 bg-white rounded-full group-hover:bg-red-100 transition-colors">
               <X size={12} />
            </div>
          </button>
        ))}

        <button 
          onClick={onClear}
          className="text-xs font-bold text-slate-400 hover:text-slate-600 hover:underline px-2 transition-colors"
        >
          Clear All
        </button>
      </div>

    </div>
  );
}
