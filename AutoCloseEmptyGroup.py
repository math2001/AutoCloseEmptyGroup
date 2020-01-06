import sublime
import sublime_plugin


class AutoCloseEmptyGroup(sublime_plugin.EventListener):
    def on_pre_close(self, view):
        # a hack to detect tabless views, see comment below
        # press alt+shift+2. Do you see the empty view on the right? That's
        # what I call a tabless view.
        # It doesn't have a tab, but ST still sees it as a view
        window = view.window()
        if window is None:
            return

        if view not in window.views():
            view.settings().set("auto_close_empty_group_is_tabless_view", True)

    def on_close(self, view):
        # A closed even is triggered for tabless views when an actual file
        # is opened. Without this check, the pane that the edit_settings
        # command created was automatically closed
        if view.settings().get("auto_close_empty_group_is_tabless_view") is True:
            return

        window = sublime.active_window()
        for group in range(window.num_groups()):
            if len(window.views_in_group(group)) == 0:
                window.run_command("close_pane")
                return
