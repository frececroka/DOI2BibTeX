import sublime, sublime_plugin
import urllib.request
import urllib.error
import threading

class DoiToBibtexCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel('DOI', '10.1038/nrd842', self.onDone, None, None)

	def onDone(self, doi):
		threading.Thread(target=self.fetchAndInsert, args=(doi,)).start()

	def fetchAndInsert(self, doi):
		req = urllib.request.Request('http://dx.doi.org/' + doi)
		req.add_header('accept', 'text/bibliography; style=bibtex')
		try:
			with urllib.request.urlopen(req) as res:
				bibtex = res.read().decode('utf-8').strip()
			self.window.active_view().run_command('insert', { 'characters': bibtex })
		except urllib.error.HTTPError as e:
			if e.code == 404:
				self.window.active_view().show_popup('DOI not found.')
			else:
				raise
