import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<!-- ==================== VIEW 2: INTERVIEW ROOM ==================== -->'
end_marker = '<!-- ==================== VIEW 3: RESULTS & ANALYSIS ==================== -->'

if start_marker not in content or end_marker not in content:
    print("Markers not found!")
    sys.exit(1)

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

new_view = '''<!-- ==================== VIEW 2: INTERVIEW ROOM ==================== -->
        <div id="view-interview" class="view-section hide flex flex-col xl:flex-row gap-6 min-h-[70vh]">
            
            <!-- Left Panel: Main Question Area -->
            <div class="flex-grow flex flex-col w-full xl:w-[75%] max-w-4xl relative">
                <!-- Header bài test -->
                <div class="mb-6 flex flex-col sm:flex-row sm:justify-between items-start sm:items-end gap-2">
                    <span class="font-tech text-sm text-gray-500 dark:text-gray-400 uppercase tracking-widest" id="q-category">Hạng mục: ...</span>
                    <span class="font-display font-bold text-lg text-neon-purple xl:hidden self-end" id="q-counter-mobile">1 / 100</span>
                </div>
                <!-- Progress Bar -->
                <div class="w-full bg-gray-200 dark:bg-gray-800 h-2.5 rounded-full overflow-hidden mb-6 shadow-inner">
                    <div id="q-progress" class="progress-bar-inner h-full w-0 transition-all duration-300 ease-out bg-gradient-to-r from-neon-blue to-neon-purple"></div>
                </div>

                <!-- Question Area -->
                <div class="glass-panel flex-grow p-6 md:p-8 lg:p-10 flex flex-col relative rounded-2xl shadow-lg border border-gray-200/50 dark:border-white/10 backdrop-blur-md">
                    <!-- Flag Badge in Corner -->
                    <div id="q-flag-badge" class="absolute top-4 right-4 hidden bg-yellow-100 dark:bg-yellow-400/20 text-yellow-700 dark:text-yellow-400 border border-yellow-400/30 px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 shadow-sm transform transition-all duration-300">
                        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z"></path></svg>
                        Đang phân vân
                    </div>
                    
                    <h2 id="q-text" class="text-xl md:text-2xl lg:text-3xl lg:leading-[1.6] font-medium leading-relaxed mb-8 dark:text-white mt-4 xl:mt-2 text-gray-800 transition-colors duration-300">Đang tải dữ liệu...</h2>
                    
                    <div id="q-options" class="grid grid-cols-1 gap-3 md:gap-4 flex-grow mb-6">
                        <!-- Render options here via JS -->
                    </div>
                </div>

                <!-- Controls -->
                <div class="mt-6 flex flex-col sm:flex-row gap-4 justify-between items-center bg-white/40 dark:bg-black/20 p-4 rounded-xl border border-gray-200/50 dark:border-white/5 backdrop-blur-sm shadow-sm">
                    <button id="btn-prev" onclick="app.prevQuestion()" class="w-full sm:w-auto px-6 py-3 rounded-xl border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 shadow-sm transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2 group">
                        <svg class="w-4 h-4 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                        Quay lại
                    </button>
                    
                    <button id="btn-flag" onclick="app.toggleFlag()" class="w-full sm:w-auto px-6 py-3 rounded-xl border-2 border-yellow-400/50 dark:border-yellow-500/50 text-yellow-700 dark:text-yellow-400 hover:bg-yellow-50 dark:hover:bg-yellow-500/10 font-bold shadow-sm transition-all flex justify-center items-center gap-2 hover:scale-[1.02] active:scale-[0.98]">
                        <svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
                        <span id="btn-flag-text">Đánh dấu Phân vân</span>
                    </button>
                    
                    <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                        <button id="btn-next" onclick="app.nextQuestion()" class="w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-neon-blue to-neon-purple text-white font-bold shadow-lg hover:shadow-[0_0_20px_rgba(0,243,255,0.4)] transition-all hover:-translate-y-0.5 active:translate-y-0 flex justify-center items-center gap-2 group">
                            Tiếp tục
                            <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                        </button>
                        <button id="btn-finish" onclick="app.finishInterview()" class="hide w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-red-600 to-rose-500 hover:from-red-500 hover:to-rose-400 text-white font-bold shadow-[0_0_15px_rgba(255,0,0,0.4)] transition-all hover:-translate-y-0.5 flex justify-center items-center gap-2 group">
                            Nộp bài
                            <svg class="w-4 h-4 transform group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right Panel: Navigator Grid -->
            <!-- Mobile: Toggleable drawer; Desktop: Sticky Sidebar -->
            <div class="w-full xl:w-[25%] flex flex-col">
                <div class="glass-panel p-4 flex flex-col xl:sticky xl:top-24 xl:h-[calc(100vh-8rem)] rounded-2xl shadow-lg border border-gray-200/50 dark:border-white/10 z-10 transition-all duration-300">
                    <div class="flex justify-between items-center mb-4 border-b border-gray-200/60 dark:border-gray-700/60 pb-3 cursor-pointer xl:cursor-default" onclick="if(window.innerWidth < 1280) app.toggleGridMobile()">
                        <h3 class="font-display font-bold text-gray-800 dark:text-white flex items-center gap-2">
                            <svg class="w-5 h-5 text-neon-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
                            Danh Sách 100 Câu
                        </h3>
                        <span class="font-display font-bold text-lg text-neon-purple hidden xl:block" id="q-counter-desktop">1 / 100</span>
                        
                        <!-- Mobile Toggle Button -->
                        <button id="btn-toggle-grid" class="xl:hidden p-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors flex items-center">
                            <span class="font-bold text-sm mr-2 text-neon-purple" id="q-counter-mobile-toggle">1/100</span>
                            <svg class="w-5 h-5 transition-transform duration-300" id="icon-toggle-grid" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                    </div>
                    
                    <div id="grid-content" class="flex flex-col xl:flex-grow flex-grow-0 overflow-hidden transition-all duration-300 ease-in-out max-h-0 opacity-0 xl:!max-h-[1000px] xl:!opacity-100">
                        <!-- Legend -->
                        <div class="flex flex-wrap gap-x-3 gap-y-2 mb-4 text-[11px] sm:text-xs font-tech text-gray-600 dark:text-gray-400 justify-center xl:justify-start">
                            <div class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-sm bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-600"></div> Chưa làm</div>
                            <div class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-sm bg-green-500/20 border border-green-500 text-green-500 flex items-center justify-center"><svg class="w-2 h-2 opacity-80" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"></path></svg></div> Đã làm</div>
                            <div class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-sm bg-neon-blue border border-neon-blue shadow-[0_0_5px_rgba(0,243,255,0.6)]"></div> Đang chọn</div>
                            <div class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-sm bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 relative"><div class="absolute right-0 top-0 -mt-1 -mr-1 w-2 h-2 rounded-full bg-yellow-400 shadow-[0_0_5px_rgba(250,204,21,1)]"></div></div> Phân vân</div>
                        </div>
                        
                        <style>
                            .custom-scrollbar::-webkit-scrollbar { width: 5px; }
                            .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
                            .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.4); border-radius: 10px; }
                            .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(107, 114, 128, 0.6); }
                        </style>
                        
                        <!-- Grid Matrix -->
                        <div class="flex-grow overflow-y-auto pr-2 pb-4 custom-scrollbar">
                            <div id="q-nav-grid" class="grid grid-cols-5 sm:grid-cols-10 xl:grid-cols-5 gap-1.5 auto-rows-max pb-2">
                                <!-- JS generates buttons here -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== VIEW 3: RESULTS & ANALYSIS ==================== -->
'''

new_content = content[:start_idx] + new_view + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("done html")
