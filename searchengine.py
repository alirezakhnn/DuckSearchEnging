import tkinter as tk
import webbrowser
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

root = tk.Tk()
root.title("Search Engine")
root.configure(bg="#1E1E1E")
root.geometry("900x600")

# Focus on query entry field on startup
root.focus_force()

search_frame = tk.Frame(root, bg="#1E1E1E")
search_frame.pack(padx=10, pady=10)

query_entry = tk.Entry(search_frame, width=50, font=("Helvetica", 14), bg="#333333", fg="#FFFFFF")
query_entry.pack(side=tk.LEFT)
query_entry.focus()

submit_button = tk.Button(search_frame, text="\u2315", font=("Helvetica", 14), bg="#007ACC", fg="#FFFFFF", command=lambda: search())
submit_button.pack(side=tk.LEFT, padx=10)

results_frame = tk.Frame(root, bg="#1E1E1E")
results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

results_canvas = tk.Canvas(results_frame, bg="#1E1E1E", highlightthickness=0)
results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

results_scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_canvas.yview)
results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results_canvas.configure(yscrollcommand=results_scrollbar.set)

results_frame_inner = tk.Frame(results_canvas, bg="#1E1E1E")
results_canvas.create_window((0, 0), window=results_frame_inner, anchor="nw")

loading_label = tk.Label(results_frame_inner, text="Loading...", bg="#1E1E1E", fg="#FFFFFF")
no_results_label = tk.Label(results_frame_inner, text="No results found.", bg="#1E1E1E", fg="#FFFFFF")

def search(*args):
    show_loading_indicator()
    query = query_entry.get()
    results = perform_search(query)
    display_results(results)


def show_loading_indicator():
    loading_label.pack(pady=10)
    root.update()


def hide_loading_indicator():
    loading_label.pack_forget()
    root.update()


def perform_search(query):
    # Create URL for DuckDuckGo search
    url_query = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={url_query}"

    # Download search results HTML
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract search result links
    results = []
    for result in soup.find_all('a', class_='result__url'):
        link = result['href']
        results.append(link)

    return results


def display_results(results):
    global results_frame_inner
    results_frame_inner.destroy()
    results_frame_inner = tk.Frame(results_canvas, bg="#1E1E1E")
    results_canvas.create_window((0, 0), window=results_frame_inner, anchor="nw")

    if len(results) == 0:
        no_results_label.pack(pady=10)
    else:
        # Create a new frame to center the link labels within the canvas
        center_frame = tk.Frame(results_frame_inner, bg="#1E1E1E")
        center_frame.pack(expand=True)

        for i, result in enumerate(results):
            result_label = tk.Label(center_frame, text=result, font=("Helvetica", 12), fg="#007ACC", cursor="hand2", bg="#1E1E1E", justify='center')
            result_label.pack(pady=5)
            result_label.bind("<Button-1>", lambda e, link=result: webbrowser.open_new(link))

    hide_loading_indicator()

    # Update canvas scroll region
    results_frame_inner.update_idletasks()
    results_canvas.config(scrollregion=results_canvas.bbox("all"))



# Bind <Return> event to search() function
root.bind("<Return>", search)

root.mainloop()
