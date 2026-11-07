import React, { type ReactNode, useEffect } from 'react';
import FloatingAssistant from '@site/src/components/FloatingAssistant/FloatingAssistant';
import ReadingProgressBar from '@site/src/components/ReadingProgressBar/ReadingProgressBar';

// Import D3 transition & selection to ensure prototype methods exist
import 'd3-transition';
import { selection } from 'd3-selection';

// ---------------------------------------------------------------------------
// Bulletproof polyfill for Mermaid D3 tooltip transition
// Prevents "TypeError: tooltipElem.transition is not a function"
// ---------------------------------------------------------------------------
if (typeof window !== 'undefined') {
  try {
    const proto = (selection as any)?.prototype;
    if (proto && typeof proto.transition !== 'function') {
      proto.transition = function () {
        const self = this;
        const proxy: any = {
          duration: () => proxy,
          delay: () => proxy,
          ease: () => proxy,
          style: (name: string, value: any) => {
            try { self.style(name, value); } catch {}
            return proxy;
          },
          attr: (name: string, value: any) => {
            try { self.attr(name, value); } catch {}
            return proxy;
          },
          text: (value: any) => {
            try { self.text(value); } catch {}
            return proxy;
          },
          html: (value: any) => {
            try { self.html(value); } catch {}
            return proxy;
          },
          on: (type: string, listener: any) => {
            try { self.on(type, listener); } catch {}
            return proxy;
          },
          remove: () => {
            try { self.remove(); } catch {}
            return proxy;
          },
        };
        return proxy;
      };
    }
  } catch (err) {
    // Non-critical fallback suppression
  }
}

/**
 * Root component wrapping every page in the Docusaurus site.
 * Provides global reading progress bar, persistent Pro-Max AI Assistant,
 * and resilient D3 tooltip error prevention.
 */
export default function Root({ children }: { children: ReactNode }): ReactNode {
  useEffect(() => {
    // Window-level safety net for any async D3 selection instances
    if (typeof window !== 'undefined') {
      try {
        const proto = (selection as any)?.prototype;
        if (proto && typeof proto.transition !== 'function') {
          proto.transition = function () {
            const self = this;
            const proxy: any = {
              duration: () => proxy,
              delay: () => proxy,
              ease: () => proxy,
              style: (name: string, value: any) => {
                try { self.style(name, value); } catch {}
                return proxy;
              },
              attr: (name: string, value: any) => {
                try { self.attr(name, value); } catch {}
                return proxy;
              },
              text: (value: any) => {
                try { self.text(value); } catch {}
                return proxy;
              },
              html: (value: any) => {
                try { self.html(value); } catch {}
                return proxy;
              },
              on: (type: string, listener: any) => {
                try { self.on(type, listener); } catch {}
                return proxy;
              },
              remove: () => {
                try { self.remove(); } catch {}
                return proxy;
              },
            };
            return proxy;
          };
        }
      } catch {}
    }
  }, []);

  return (
    <>
      <ReadingProgressBar />
      {children}
      <FloatingAssistant />
    </>
  );
}
