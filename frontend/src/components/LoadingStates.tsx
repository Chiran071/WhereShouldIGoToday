'use client';

export function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        {/* Outer ring */}
        <div className="w-20 h-20 rounded-full border-4 border-himalaya-200 animate-pulse"></div>
        
        {/* Inner spinning ring */}
        <div className="absolute inset-0 w-20 h-20 rounded-full border-4 border-transparent border-t-primary-500 animate-spin"></div>
        
        {/* Center icon */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-3xl animate-bounce-gentle">🏔️</span>
        </div>
      </div>
      
      <p className="mt-6 text-himalaya-600 font-medium animate-pulse">
        Finding your perfect spot...
      </p>
      
      <div className="flex gap-1 mt-3">
        <span className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
        <span className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
        <span className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
      </div>
    </div>
  );
}

export function EmptyState() {
  return (
    <div className="text-center py-16">
      <div className="text-6xl mb-4">🤔</div>
      <h3 className="text-xl font-semibold text-himalaya-800 mb-2">
        No recommendations yet
      </h3>
      <p className="text-himalaya-500">
        Fill in your preferences above and hit "Find My Spot!"
      </p>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="text-center py-16 bg-red-50 rounded-2xl">
      <div className="text-6xl mb-4">😕</div>
      <h3 className="text-xl font-semibold text-red-800 mb-2">
        Oops! Something went wrong
      </h3>
      <p className="text-red-600 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="bg-red-500 text-white px-6 py-2 rounded-xl font-medium hover:bg-red-600 transition-all"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
