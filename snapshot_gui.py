# import os
# import tkinter as tk
# from tkinter import messagebox, ttk

# from snapshot_manager import create_snapshot, delete_snapshot, list_snapshots, rollback_snapshot

# class SnapshotManagerWindow:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Enterprise Snapshot Manager")
#         self.root.geometry("1000x720")
#         self.root.minsize(900, 600)
#         self.root.configure(bg="#07111f")
#         self.root.option_add("*Font", ("Sans", 10))
        
#         # ... (ကျန်တဲ့ မင်းရဲ့ မူရင်း UI Code တွေ ဒီအောက်မှာ ဆက်ထားပါ)


#         # --- Header Section ---
#         header = tk.Frame(root, bg="#111c31", bd=1, relief="raised", padx=20, pady=14)
#         header.pack(fill="x", padx=20, pady=(16, 8))

#         tk.Label(header, text="VERSIONED SNAPSHOT MANAGEMENT", bg="#111c31", fg="#7dd3fc", font=("Sans", 16, "bold")).pack(anchor="w")
#         tk.Label(header, text="Create, review, rollback, or delete snapshot versions for your protected files.", bg="#111c31", fg="#94a3b8", font=("Sans", 9)).pack(anchor="w", pady=(2, 0))

#         # --- Control Input Frame ---
#         control_frame = tk.Frame(root, bg="#111c31", bd=1, relief="raised", padx=16, pady=10)
#         control_frame.pack(fill="x", padx=20, pady=6)

#         lbl_input = tk.Label(control_frame, text="Snapshot Label:", bg="#111c31", fg="#94a3b8", font=("Sans", 9, "bold"))
#         lbl_input.pack(side="left", padx=(0, 8))

#         self.label_entry = tk.Entry(control_frame, width=28, font=("Sans", 10))
#         self.label_entry.insert(0, "manual")
#         self.label_entry.pack(side="left", padx=(0, 12))

#         btn_create = tk.Button(control_frame, text="Create Snapshot", command=self.create_snapshot, bg="#10b981", fg="white", font=("Sans", 10, "bold"), padx=10, pady=4)
#         btn_create.pack(side="left", padx=4)

#         btn_refresh = tk.Button(control_frame, text="Refresh List", command=self.refresh_list, bg="#3b82f6", fg="white", font=("Sans", 10, "bold"), padx=10, pady=4)
#         btn_refresh.pack(side="left", padx=4)

#         # --- Action Buttons ---
#         action_frame = tk.Frame(root, bg="#07111f", padx=20, pady=6)
#         action_frame.pack(side="bottom", fill="x", pady=(0, 16))

#         btn_rollback = tk.Button(action_frame, text="ROLLBACK SELECTED", command=self.rollback_selected, bg="#f59e0b", fg="white", font=("Sans", 10, "bold"), padx=12, pady=6, width=25)
#         btn_rollback.grid(row=0, column=0, padx=6, pady=4, sticky="ew")

#         btn_delete = tk.Button(action_frame, text="DELETE SELECTED", command=self.delete_selected, bg="#ef4444", fg="white", font=("Sans", 10, "bold"), padx=12, pady=6, width=25)
#         btn_delete.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

#         btn_open = tk.Button(action_frame, text="OPEN TEST FILES FOLDER", command=self.open_files, bg="#8b5cf6", fg="white", font=("Sans", 10, "bold"), padx=12, pady=6, width=25)
#         btn_open.grid(row=0, column=2, padx=6, pady=4, sticky="ew")

#         for col in range(3):
#             action_frame.columnconfigure(col, weight=1)

#         # --- Treeview Table Frame ---
#         tree_frame = tk.Frame(root, bg="#111c31", bd=1, relief="raised", padx=12, pady=10)
#         tree_frame.pack(side="top", fill="both", expand=True, padx=20, pady=6)

#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("Treeview", background="#020617", foreground="#7dd3fc", fieldbackground="#020617", font=("Monospace", 10), rowheight=24)
#         style.configure("Treeview.Heading", background="#111c31", foreground="#f8fafc", font=("Sans", 10, "bold"))

#         columns = ("version", "name", "created_at")
#         self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
#         self.tree.heading("version", text="Version")
#         self.tree.heading("name", text="Snapshot Name")
#         self.tree.heading("created_at", text="Created At")

#         self.tree.column("version", width=80, anchor="center")
#         self.tree.column("name", width=460, anchor="w")
#         self.tree.column("created_at", width=220, anchor="center")
#         scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scrollbar.set)

#         self.tree.pack(side="left", fill="both", expand=True)
#         scrollbar.pack(side="right", fill="y")

#         self.refresh_list()

#     def create_snapshot(self):
#         label = self.label_entry.get().strip() or "manual"
#         snapshot = create_snapshot(label=label)
#         self.refresh_list()
#         messagebox.showinfo("Snapshot Created", f"Snapshot Version {snapshot['version']} created successfully.")

#     def refresh_list(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)

#         snapshots = list_snapshots()
#         for snapshot in snapshots:
#             self.tree.insert("", "end", values=(snapshot["version"], snapshot["name"], snapshot["created_at"]))

#     # def rollback_selected(self):
#     #     selected = self.tree.selection()
#     #     if not selected:
#     #         messagebox.showwarning("No Selection", "Please select a snapshot row from the table to rollback.")
#     #         return

#     #     item = self.tree.item(selected[0])
#     #     version = item["values"][0]
#     #     if messagebox.askyesno("Confirm Rollback", f"Are you sure you want to restore test files to snapshot version {version}?"):
#     #         ok = rollback_snapshot(version=int(version))
#     #         if ok:
#     #             messagebox.showinfo("Rollback Complete", f"Test files successfully restored from snapshot version {version}.")
#     #         else:
#     #             messagebox.showerror("Rollback Failed", f"Snapshot version {version} could not be restored.")
#     #1
#     # def rollback_selected(self):
#     #     selected = self.tree.selection()
#     #     if not selected:
#     #         messagebox.showwarning("No Selection", "Please select a snapshot row from the table to rollback.")
#     #         return

#     #     item = self.tree.item(selected[0])
#     #     version = item["values"][0]
#     #     if messagebox.askyesno("Confirm Rollback", f"Are you sure you want to restore test files to snapshot version {version}?"):
#     #         result = rollback_snapshot(version=int(version))
#     #         if result["success"]:
#     #             msg = f"Restored test files from snapshot version {version}.\n\n"
#     #             msg += f" SHA-256 Data Integrity Check:\n"
#     #             msg += f"Files Verified: {result['verified_count']}\n\n"
#     #             msg += f"Hash Verification Logs:\n{result['logs']}"
#     #             messagebox.showinfo("Rollback & Hash Verified", msg)
#     #         else:
#     #             messagebox.showerror("Rollback Failed", result["message"])
# #2


#     def delete_selected(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showwarning("No Selection", "Please select a snapshot row to delete.")
#             return

#         item = self.tree.item(selected[0])
#         version = item["values"][0]
#         if messagebox.askyesno("Confirm Deletion", f"Permanently delete snapshot version {version}?"):
#             ok = delete_snapshot(version=int(version))
#             if ok:
#                 self.refresh_list()
#                 messagebox.showinfo("Deleted", f"Snapshot version {version} removed successfully.")
#             else:
#                 messagebox.showerror("Delete Failed", f"Snapshot version {version} could not be deleted.")

#     def open_files(self):
#         target_dir = "test_files"
#         if not os.path.exists(target_dir):
#             os.makedirs(target_dir)
#         os.system(f"xdg-open {target_dir} > /dev/null 2>&1")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SnapshotManagerWindow(root)
#     root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from unittest import result
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
        self.root.geometry("700x500")

        # Title Block
        header_frame = ttk.Frame(self.root, padding=15)
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(
            header_frame,
            text="VERSIONED SNAPSHOT MANAGEMENT",
            font=("Helvetica", 14, "bold"),
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = ttk.Label(
            header_frame,
            text=(
                "Create, review, rollback, or delete snapshot versions for"
                " your protected files."
            ),
            font=("Helvetica", 9),
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Controls
        ctrl_frame = ttk.Frame(self.root, padding=(15, 0, 15, 10))
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Snapshot Label:").pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.label_entry = ttk.Entry(ctrl_frame, width=20)
        self.label_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.label_entry.insert(0, "manual")

        create_btn = ttk.Button(
            ctrl_frame, text="Create Snapshot", command=self.create_new
        )
        create_btn.pack(side=tk.LEFT, padx=(0, 5))

        refresh_btn = ttk.Button(
            ctrl_frame, text="Refresh List", command=self.refresh_list
        )
        refresh_btn.pack(side=tk.LEFT)

        # Treeview Table
        table_frame = ttk.Frame(self.root, padding=15)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("version", "name", "created_at")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("version", text="Version")
        self.tree.heading("name", text="Snapshot Name")
        self.tree.heading("created_at", text="Created At")

        self.tree.column("version", width=70, anchor=tk.CENTER)
        self.tree.column("name", width=380, anchor=tk.W)
        self.tree.column("created_at", width=180, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action Buttons
        btn_frame = ttk.Frame(self.root, padding=15)
        btn_frame.pack(fill=tk.X)

        rollback_btn = ttk.Button(
            btn_frame, text="ROLLBACK SELECTED", command=self.rollback_selected
        )
        rollback_btn.pack(side=tk.LEFT, padx=(0, 10))

        delete_btn = ttk.Button(
            btn_frame, text="DELETE SELECTED", command=self.delete_selected
        )
        delete_btn.pack(side=tk.RIGHT)

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
        label = self.label_entry.get().strip()
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
            f"Are you sure you want to restore test files to snapshot version"
            f" {version}?",
        ):
            result = rollback_snapshot(version=int(version))
            if result["success"]:
                # Custom Window ပြုလုပ်ခြင်း
                dialog = tk.Toplevel(self.root)
                dialog.title("Rollback & Data Integrity Report")
                dialog.geometry("580x450")

                title_lbl = ttk.Label(
                    dialog,
                    text=f"Restored Snapshot Version {version}",
                    font=("Helvetica", 12, "bold"),
                )
                title_lbl.pack(pady=(15, 5))

                sub_lbl = ttk.Label(
                    dialog,
                    text=(
                        f" SHA-256 Verified Files: {result['verified_count']}"
                    ),
                    font=("Helvetica", 10),
                )
                sub_lbl.pack(pady=(0, 10))

                frame = ttk.Frame(dialog)
                frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

                text_area = tk.Text(
                    frame, wrap=tk.WORD, font=("Consolas", 10), bg="#f8f9fa"
                )
                scrollbar = ttk.Scrollbar(
                    frame, orient=tk.VERTICAL, command=text_area.yview
                )
                text_area.configure(yscrollcommand=scrollbar.set)

                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                # Color Tags သတ်မှတ်ခြင်း (အနီရောင် နှင့် အစိမ်းရောင်)
                text_area.tag_config(
                    "mismatch",
                    foreground="red",
                    font=("Consolas", 10, "bold"),
                )
                text_area.tag_config("verified", foreground="green")
            for line in result["logs"].split("\n"):
                    if "Hash Mismatch" in line or "" in line:
                        text_area.insert(tk.END, line + "\n", "mismatch")
                    elif "Verified" in line or "" in line:
                        text_area.insert(tk.END, line + "\n", "verified")
                    else:
                        text_area.insert(tk.END, line + "\n")

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
            f"Are you sure you want to permanently delete snapshot version"
            f" {version}?",
        ):
            ok = delete_snapshot(version=int(version))
            if ok:
                self.refresh_list()
                messagebox.showinfo(
                    "Deleted", f"Snapshot version {version} deleted."
                )
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete snapshot version {version}."
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = SnapshotGUI(root)
    root.mainloop()