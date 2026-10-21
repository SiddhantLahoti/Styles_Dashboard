import React from 'react';
import MultiSelectDropdown from './MultiSelectDropdown';

export default function FilterSidebar({
  options = {},
  filters = {},
  onFilterChange,
  onReset,
  onShortlistAllFiltered,
  shortlistAllBtnText,
}) {
  return (
    <aside className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4 h-fit">
      {/* Header */}
      <div className="flex justify-between items-center pb-2 border-b">
        <h2 className="font-semibold text-sm uppercase text-slate-700 tracking-wider">Filters</h2>
        <button
          type="button"
          onClick={onReset}
          className="text-xs text-indigo-600 hover:underline font-medium"
        >
          Reset All
        </button>
      </div>

      {/* Shortlist All Button */}
      <button
        type="button"
        onClick={onShortlistAllFiltered}
        className="w-full py-2 px-3 text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg border border-amber-300 flex items-center justify-center gap-1.5 shadow-sm transition-colors"
      >
        <span>{shortlistAllBtnText || '⭐ Shortlist All Filtered Results'}</span>
      </button>

      {/* File A Filters */}
      <MultiSelectDropdown
        label="Category"
        defaultLabel="All Categories"
        options={options.categories || []}
        selected={filters.category || []}
        onChange={(val) => onFilterChange('category', val)}
      />

      <MultiSelectDropdown
        label="Sales Category 1"
        defaultLabel="All Sales Cat 1"
        options={options.sales_categories1 || []}
        selected={filters.sales_cat1 || []}
        onChange={(val) => onFilterChange('sales_cat1', val)}
      />

      <MultiSelectDropdown
        label="Sales Category 2"
        defaultLabel="All Sales Cat 2"
        options={options.sales_categories2 || []}
        selected={filters.sales_cat2 || []}
        onChange={(val) => onFilterChange('sales_cat2', val)}
      />

      <MultiSelectDropdown
        label="Brand"
        defaultLabel="All Brands"
        options={options.brands || []}
        selected={filters.brand || []}
        onChange={(val) => onFilterChange('brand', val)}
      />

      <MultiSelectDropdown
        label="Tone"
        defaultLabel="All Tones"
        options={options.tones || []}
        selected={filters.tone || []}
        onChange={(val) => onFilterChange('tone', val)}
      />

      <MultiSelectDropdown
        label="Set Code"
        defaultLabel="All Set Codes"
        options={options.set_codes || []}
        selected={filters.set_cd || []}
        onChange={(val) => onFilterChange('set_cd', val)}
      />

      <MultiSelectDropdown
        label="Customer"
        defaultLabel="All Customers"
        options={options.customers || []}
        selected={filters.customer || []}
        onChange={(val) => onFilterChange('customer', val)}
      />

      {/* Metal & Color Grid */}
      <div className="grid grid-cols-2 gap-2">
        <MultiSelectDropdown
          label="Metal"
          defaultLabel="All"
          maxHeightClass="max-h-36"
          options={options.metals || []}
          selected={filters.metal || []}
          onChange={(val) => onFilterChange('metal', val)}
        />
        <MultiSelectDropdown
          label="Color"
          defaultLabel="All"
          maxHeightClass="max-h-36"
          options={options.colors || []}
          selected={filters.color || []}
          onChange={(val) => onFilterChange('color', val)}
        />
      </div>

      <MultiSelectDropdown
        label="Concept Designer"
        defaultLabel="All Concept By"
        options={options.concept_designers || []}
        selected={filters.concept_by || []}
        onChange={(val) => onFilterChange('concept_by', val)}
      />

      <MultiSelectDropdown
        label="Weight Designer"
        defaultLabel="All Weight By"
        options={options.weight_designers || []}
        selected={filters.weight_by || []}
        onChange={(val) => onFilterChange('weight_by', val)}
      />

      {/* Creation Date Range */}
      <div>
        <label className="block text-xs font-medium text-slate-600 mb-1">Creation Date</label>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="date"
            value={filters.start_date || ''}
            onChange={(e) => onFilterChange('start_date', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <input
            type="date"
            value={filters.end_date || ''}
            onChange={(e) => onFilterChange('end_date', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Total Weight Min/Max */}
      <div>
        <label className="block text-xs font-medium text-slate-600 mb-1">Total Weight (g)</label>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            step="0.001"
            placeholder="Min"
            value={filters.min_total_wt ?? ''}
            onChange={(e) => onFilterChange('min_total_wt', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <input
            type="number"
            step="0.001"
            placeholder="Max"
            value={filters.max_total_wt ?? ''}
            onChange={(e) => onFilterChange('max_total_wt', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* File B Raw Material Divider */}
      <div className="pt-3 border-t border-slate-200">
        <span className="text-[11px] font-bold text-indigo-700 uppercase tracking-wider block mb-2">
          💎 Stones & Raw Materials
        </span>
      </div>

      <MultiSelectDropdown
        label="Stone Type (Ctg)"
        defaultLabel="All Types"
        maxHeightClass="max-h-36"
        options={options.rm_categories || []}
        selected={filters.rm_category || []}
        onChange={(val) => onFilterChange('rm_category', val)}
      />

      <MultiSelectDropdown
        label="Stone Shape (SubCtg)"
        defaultLabel="All Shapes"
        options={options.rm_subcategories || []}
        selected={filters.rm_subcategory || []}
        onChange={(val) => onFilterChange('rm_subcategory', val)}
      />

      {/* Sieve Sizes */}
      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Sieve Size 1 (Ln1)</label>
          <input
            type="number"
            step="0.001"
            placeholder="e.g. 1.50"
            value={filters.ln1 ?? ''}
            onChange={(e) => onFilterChange('ln1', e.target.value)}
            className="w-full text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Sieve Size 2 (Ln2)</label>
          <input
            type="number"
            step="0.001"
            placeholder="e.g. 2.00"
            value={filters.ln2 ?? ''}
            onChange={(e) => onFilterChange('ln2', e.target.value)}
            className="w-full text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Stone Weight */}
      <div>
        <label className="block text-xs font-medium text-slate-600 mb-1">Stone Weight (RmWt in Cts)</label>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            step="0.001"
            placeholder="Min"
            value={filters.min_rm_wt ?? ''}
            onChange={(e) => onFilterChange('min_rm_wt', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <input
            type="number"
            step="0.001"
            placeholder="Max"
            value={filters.max_rm_wt ?? ''}
            onChange={(e) => onFilterChange('max_rm_wt', e.target.value)}
            className="text-xs border border-slate-300 rounded-lg p-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>
    </aside>
  );
}