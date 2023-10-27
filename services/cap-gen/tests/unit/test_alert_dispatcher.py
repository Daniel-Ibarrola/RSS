import datetime
import queue

from rss.cap.alert import Alert

from capgen.services import AlertDispatcher


class TestAlertDispatcher:

    def test_dispatch_alerts(self):
        initial_alert = Alert(
            time=datetime.datetime.now(),
            states=[40],
            region=41203,
            id="TESTALERT"
        )
        alerts = queue.Queue()
        alerts.put(initial_alert)
        dispatcher = AlertDispatcher(alerts)
        dispatcher._dispatch_alerts()

        assert alerts.empty()

        alert_write = dispatcher.to_write.get()
        assert dispatcher.to_write.empty()
        assert alert_write == initial_alert

        alert_post = dispatcher.to_post.get()
        assert dispatcher.to_post.empty()
        assert alert_post == initial_alert
        assert alert_post is not alert_write
