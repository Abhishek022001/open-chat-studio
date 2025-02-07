import { newSpecPage } from '@stencil/core/testing';
import { OcsChat } from '../ocs-chat';
import {h} from "@stencil/core";

describe('open-chat-studio-widget', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [OcsChat],
      html: `<open-chat-studio-widget></open-chat-studio-widget>`,
    });
    expect(page.root).toEqualHtml(`
      <open-chat-studio-widget>
        <mock:shadow-root>
          <button class="btn">Chat</button>
        </mock:shadow-root>
      </open-chat-studio-widget>
    `);
  });

  it('renders with visible', async () => {
    const page = await newSpecPage({
      components: [OcsChat],
      html: `<open-chat-studio-widget visible="true"></open-chat-studio-widget>`,
    });
    expect(page.root).toEqualHtml(`
      <open-chat-studio-widget visible="true">
        <mock:shadow-root>
          <button class="btn">Chat</button>
          <div class="fixed w-[450px] h-3/5 bg-white border border-gray-200 shadow-lg rounded-lg overflow-hidden flex flex-col bottom-5 right-5 ">
            <div class="flex justify-between items-center px-2 py-2 border-b border-gray-100">
              <div class="flex gap-1">
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Dock to left"
                  title="Dock to left"
                >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                     class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75"/>
                </svg>
                </button>
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Center"
                  title="Center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
                  </svg>
                </button>
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-blue-600"
                  aria-label="Dock to right"
                  title="Dock to right"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15M12 9l3 3m0 0-3 3m3-3H2.25"/>
                  </svg>
                </button>
              </div>
              <div class="flex gap-1">
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Expand"
                  title="Expand"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"/>
                  </svg>
                </button>
                <button
                  class="p-1.5 hover:bg-gray-100 rounded-md transition-colors duration-200 text-gray-500"
                  aria-label="Close"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>
            <iframe class="flex-grow w-full border-none iframe-placeholder"></iframe>
          </div>
        </mock:shadow-root>
      </open-chat-studio-widget>
    `);
  });

  it('renders options', async () => {
    const page = await newSpecPage({
      components: [OcsChat],
      html: `<open-chat-studio-widget visible="true" bot-url="https://localhost" position="center" expanded="true"></open-chat-studio-widget>`,
    });
    expect(page.root).toEqualHtml(`
      <open-chat-studio-widget visible="true" bot-url="https://localhost" position="center" expanded="true">
        <mock:shadow-root>
          <button class="btn">Chat</button>
          <div class="fixed w-[450px] h-5/6 bg-white border border-gray-200 shadow-lg rounded-lg overflow-hidden flex flex-col left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <div class="flex justify-between items-center px-2 py-2 border-b border-gray-100">
              <div class="flex gap-1">
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Dock to left"
                  title="Dock to left"
                >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                     class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75"/>
                </svg>
                </button>
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-blue-600"
                  aria-label="Center"
                  title="Center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
                  </svg>
                </button>
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Dock to right"
                  title="Dock to right"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15M12 9l3 3m0 0-3 3m3-3H2.25"/>
                  </svg>
                </button>
              </div>
              <div class="flex gap-1">
                <button
                  class="p-1.5 rounded-md transition-colors duration-200 hover:bg-gray-100 text-gray-500"
                  aria-label="Collapse"
                  title="Collapse"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/>
                  </svg>
                </button>
                <button
                  class="p-1.5 hover:bg-gray-100 rounded-md transition-colors duration-200 text-gray-500"
                  aria-label="Close"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>
            <iframe class="flex-grow w-full border-none iframe-placeholder" src="https://localhost"></iframe>
          </div>
        </mock:shadow-root>
      </open-chat-studio-widget>
    `);
  });
});
