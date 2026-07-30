import os
import tkinter as tk
from tkinter import messagebox, ttk
from snapshot_manager import (
    create_snapshot,
    delete_snapshot,
    list_snapshots,
    rollback_snapshot,
)


class SnapshotGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise Snapshot Manager")
        self.root.geometry("1180x730")
        self.root.minsize(980, 640)
        self.root.configure(bg="#07111f")

        # --- Custom ttk Styles for Larger & Modern Fonts ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure global fonts and dark theme color harmonization
        self.style.configure(".", font=("Sans", 11), background="#07111f", foreground="#f8fafc")
        self.style.configure("TFrame", background="#07111f")
        self.style.configure("TLabel", background="#07111f", foreground="#f8fafc")
        self.style.configure("Heading.TLabel", font=("Sans", 14, "bold"), foreground="#7dd3fc", background="#07111f")
        
        # Treeview styling with generous row height
        self.style.configure("Treeview", background="#020617", foreground="#7dd3fc", fieldbackground="#020617", font=("Consolas", 11), rowheight=34)
        self.style.configure("Treeview.Heading", background="#111c31", foreground="#f8fafc", font=("Sans", 11, "bold"))
        self.style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "white")])

        # --- Header Section ---
        header_frame = tk.Frame(self.root, bg="#111c31", bd=1, relief="raised", padx=24, pady=20)
        header_frame.pack(fill="x", padx=20, pady=(20, 12))

        title_lbl = tk.Label(
            header_frame,
            text="VERSIONED SNAPSHOT MANAGEMENT",
            bg="#111c31",
            fg="#7dd3fc",
            font=("Sans", 16, "bold"),
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            header_frame,
            text="Create, review, rollback, or delete snapshot versions for your protected files.",
            bg="#111c31",
            fg="#94a3b8",
            font=("Sans", 11),
        )
        sub_lbl.pack(anchor=tk.W, pady=(6, 0))

        # --- Controls Section ---
        ctrl_frame = tk.Frame(self.root, bg="#111c31", bd=1, relief="raised", padx=22, pady=16)
        ctrl_frame.pack(fill="x", padx=20, pady=8)

        lbl_input = tk.Label(ctrl_frame, text="Snapshot Label:", bg="#111c31", fg="#94a3b8", font=("Sans", 11, "bold"))
        lbl_input.pack(side=tk.LEFT, padx=(0, 12))

        self.label_entry = tk.Entry(ctrl_frame, width=28, font=("Sans", 11), bg="#020617", fg="#f8fafc", insertbackground="white")
        self.label_entry.pack(side=tk.LEFT, padx=(0, 16), ipady=4)
        self.label_entry.insert(0, "manual")

        btn_create = tk.Button(
            ctrl_frame, text="Create Snapshot", command=self.create_new,
            bg="#10b981", fg="white", font=("Sans", 11, "bold"), padx=16, pady=8, bd=0, cursor="hand2"
        )
        btn_create.pack(side=tk.LEFT, padx=8)

        btn_refresh = tk.Button(
            ctrl_frame, text="Refresh List", command=self.refresh_list,
            bg="#3b82f6", fg="white", font=("Sans", 11, "bold"), padx=16, pady=8, bd=0, cursor="hand2"
        )
        btn_refresh.pack(side=tk.LEFT, padx=8)

        # --- Treeview Table Section ---
        table_frame = tk.Frame(self.root, bg="#111c31", bd=1, relief="raised", padx=16, pady=16)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        columns = ("version", "name", "created_at")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("version", text="Version")
        self.tree.heading("name", text="Snapshot Name")
        self.tree.heading("created_at", text="Created At")

        # Column widths configured with generous room
        self.tree.column("version", width=110, anchor=tk.CENTER, stretch=False)
        self.tree.column("name", width=640, anchor=tk.W, stretch=True)
        self.tree.column("created_at", width=230, anchor=tk.CENTER, stretch=False)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Action Buttons Section ---
        btn_frame = tk.Frame(self.root, bg="#07111f", padx=20, pady=12)
        btn_frame.pack(side="bottom", fill="x", pady=(0, 20))

        rollback_btn = tk.Button(
            btn_frame, text="ROLLBACK SELECTED", command=self.rollback_selected,
            bg="#f59e0b", fg="white", font=("Sans", 11, "bold"), pady=10, width=28, bd=0, cursor="hand2"
        )
        rollback_btn.grid(row=0, column=0, padx=10, pady=6, sticky="ew")

        delete_btn = tk.Button(
            btn_frame, text="DELETE SELECTED", command=self.delete_selected,
            bg="#ef4444", fg="white", font=("Sans", 11, "bold"), pady=10, width=28, bd=0, cursor="hand2"
        )
        delete_btn.grid(row=0, column=1, padx=10, pady=6, sticky="ew")

        for col in range(2):
            btn_frame.columnconfigure(col, weight=1)

        # Initial load
        self.refresh_list()

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        snapshots = list_snapshots()
        for snap in snapshots:
            self.tree.insert(
                "",
                tk.END,
                values=(snap["version"], snap["name"], snap["created_at"]),
            )

    def create_new(self):
        label = self.label_entry.get().strip() or "manual"
        result = create_snapshot(label=label)
        messagebox.showinfo(
            "Snapshot Created",
            f"Created snapshot version {result['version']}:\n{result['name']}",
        )
        self.refresh_list()

    def rollback_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a snapshot row from the table to rollback.",
            )
            return
        item = self.tree.item(selected[0])
        version = item["values"][0]

        if messagebox.askyesno(
            "Confirm Rollback",
            f"Are you sure you want to restore test files to snapshot version {version}?",
        ):
            result = rollback_snapshot(version=int(version))
            if result.get("success"):
                dialog = tk.Toplevel(self.root)
                dialog.title("Rollback & Data Integrity Report")
                dialog.geometry("740x560")
                dialog.minsize(580, 420)
                dialog.configure(bg="#07111f")

                tk.Label(
                    dialog,
                    text=f"Restored Snapshot Version {version}",
                    bg="#07111f",
                    fg="#7dd3fc",
                    font=("Sans", 13, "bold"),
                ).pack(pady=(22, 6))

                tk.Label(
                    dialog,
                    text=f"SHA-256 Verified Files Count: {result.get('verified_count', 0)}",
                    bg="#07111f",
                    fg="#94a3b8",
                    font=("Sans", 11),
                ).pack(pady=(0, 14))

                frame = tk.Frame(dialog, bg="#111c31", padx=16, pady=16)
                frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)

                text_area = tk.Text(
                    frame, wrap=tk.WORD, font=("Consolas", 11), bg="#020617", fg="#f8fafc", bd=0, relief="flat"
                )
                scrollbar = ttk.Scrollbar(
                    frame, orient=tk.VERTICAL, command=text_area.yview
                )
                text_area.configure(yscrollcommand=scrollbar.set)

                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                text_area.tag_config("mismatch", foreground="#f87171", font=("Consolas", 11, "bold"))
                text_area.tag_config("verified", foreground="#4ade80")

                logs = result.get("logs", "No logs available.")
                for line in logs.split("\n"):
                    if "Mismatch" in line or "Error" in line:
                        text_area.insert(tk.END, line + "\n", "mismatch")
                    elif "Verified" in line or "Success" in line:
                        text_area.insert(tk.END, line + "\n", "verified")
                    else:
                        text_area.insert(tk.END, line + "\n")
            else:
                messagebox.showerror("Rollback Failed", result.get("message", "Unknown error occurred."))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a snapshot row from the table to delete.",
            )
            return

        item = self.tree.item(selected[0])
        version = item["values"][0]

        if messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete snapshot version {version}?",
        ):
            ok = delete_snapshot(version=int(version))
            if ok:
                self.refresh_list()
                messagebox.showinfo(
                    "Deleted", f"Snapshot version {version} deleted successfully."
                )
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete snapshot version {version}."
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = SnapshotGUI(root)
    root.mainloop()