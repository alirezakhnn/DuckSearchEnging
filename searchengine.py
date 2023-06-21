import tkinter as tk
import webbrowser
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import tkinter.ttk as ttk

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

submit_button = tk.Button(search_frame, text="\u2315", font=("Helvetica", 14), bg="#12B6FF", fg="#FFFFFF", command=lambda: search())
submit_button.pack(side=tk.LEFT, padx=10)

results_frame = tk.Frame(root, bg="#1E1E1E")
results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

results_canvas = tk.Canvas(results_frame, bg="#1E1E1E", highlightthickness=0)
results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_canvas.yview)
results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_canvas.configure(yscrollcommand=results_scrollbar.set)

loading_frame = tk.Frame(results_frame, bg="#1E1E1E")

loading_label = tk.Label(loading_frame, text="Loading...", bg="#1E1E1E", fg="#FFFFFF")

no_results_label = tk.Label(results_canvas, text="No results found.", bg="#1E1E1E", fg="#FFFFFF")

def search(*args):
    show_loading_indicator()
    query = query_entry.get()
    results = perform_search(query)
    display_results(results)


def new_search():
    query_entry.delete(0, tk.END)
    for widget in results_canvas.winfo_children():
        widget.destroy()


def show_loading_indicator():
    if loading_label.winfo_ismapped():
        return
    loading_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    loading_label.pack(side=tk.LEFT)
    root.update()



def hide_loading_indicator():
    loading_frame.pack_forget()
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
    global no_results_label
    # Clear the current search results
    for widget in results_canvas.winfo_children():
        widget.destroy()

    if len(results) == 0:
        no_results_label.pack(pady=10)
    else:
        # Create a new frame to hold the search result labels
        results_frame = tk.Frame(results_canvas, bg="#1E1E1E")
        results_frame.pack(fill=tk.BOTH, expand=True)

        for i, result in enumerate(results):
            result_label = tk.Label(results_frame, text=result, font=("Helvetica", 12), fg="#12B6FF", cursor="hand2", bg="#1E1E1E", justify='center')
            result_label.pack(pady=5)
            result_label.bind("<Button-1>", lambda event, url=result:webbrowser.open_new(url))
            
    hide_loading_indicator()

    # Pack the results frame inside the canvas
    results_canvas.create_window((0, 0), window=results_frame, anchor=tk.NW)

    # Configure the scroll region of the canvas
    results_canvas.configure(scrollregion=results_canvas.bbox("all"))

    root.update()

    
root.bind("<Return>", search)

loading_frame.pack(fill=tk.X)
root.mainloop()

