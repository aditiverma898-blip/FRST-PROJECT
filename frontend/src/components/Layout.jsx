import React from 'react';

export default function Layout({ children }) {
  return (
    <div className="bg-background text-on-background min-h-screen flex flex-col">
      {/* TopNavBar */}
      <header className="bg-surface shadow-sm sticky top-0 w-full z-50 flex justify-between items-center px-edge-margin py-stack-md max-w-container-max mx-auto">
        <div className="flex items-center gap-4">
          <img src="https://lh3.googleusercontent.com/aida/AP1WRLvbK7eP2LkB6whRhWlhcJyleAOJVQXUin2X6NMRODQMzga8ZQ2fgh0FLbUlgqACJFSId2OzIzhoojXwwDnZAtM9owvLzZUpr9V2GZJZh6N5qqL_DpWsiRe0J-p-dIrQzlGjeCzpSDeVgbnFtA6PqnbL_h9RjkAc_W-i0AWd5EMT2al6uwDE1DCuY8hyyah4hwszmUNCeKWI0TwJa4TiuTDYutbBZonwK-aSmGi7IGw3PL5IDZuhcPWFHSSM" alt="Zomato AI Logo" className="h-[40px] object-contain rounded-md" />
          <div>
            <h1 className="text-headline-md font-headline-md font-bold text-primary">Zomato AI Recommendations</h1>
            <p className="text-label-sm font-label-sm text-on-surface-variant">Find your perfect restaurant</p>
          </div>
        </div>
        <nav className="hidden md:flex gap-8 items-center">
          <a className="text-primary border-b-2 border-primary pb-1 text-label-md font-label-md transition-colors duration-200" href="#">Explore</a>
          <a className="text-on-surface-variant hover:text-primary transition-colors duration-200 text-label-md font-label-md" href="#">Bookmarks</a>
          <a className="text-on-surface-variant hover:text-primary transition-colors duration-200 text-label-md font-label-md" href="#">History</a>
        </nav>
        <div className="flex items-center">
          <button className="text-on-surface-variant hover:text-primary transition-colors duration-200">
            <span className="material-symbols-outlined" style={{ fontSize: '28px' }}>account_circle</span>
          </button>
        </div>
      </header>

      {children}

      {/* Footer */}
      <footer className="w-full py-stack-lg flex flex-col items-center gap-stack-md border-t border-outline-variant bg-surface-container-low mt-auto">
        <div className="text-label-md font-label-md font-bold text-on-surface">Zomato AI Recommendations</div>
        <div className="flex gap-4">
          <a className="text-on-surface-variant text-label-sm font-label-sm hover:text-primary transition-all" href="#">Privacy Policy</a>
          <a className="text-on-surface-variant text-label-sm font-label-sm hover:text-primary transition-all" href="#">Terms of Service</a>
          <a className="text-on-surface-variant text-label-sm font-label-sm hover:text-primary transition-all" href="#">Help Center</a>
        </div>
        <div className="text-on-surface-variant text-label-sm font-label-sm">© 2026 Zomato AI Recommendations. Powered by Culinary Intelligence.</div>
      </footer>
    </div>
  );
}
