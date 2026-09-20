"""
Módulo de agendamento interno do R.A.F.F
Substitui o Windows Task Scheduler executando verificações de horário em background.
"""

import threading
import time
from datetime import datetime, time as dtime
from typing import Callable, List, Optional, Tuple

class RaffScheduler:
    """Agendador em thread contínua que dispara callbacks em horários definidos."""

    def __init__(self, check_interval_seconds: int = 30):
        self.check_interval_seconds = check_interval_seconds
        self.schedules: List[Tuple[int, int]] = []  # Lista de (hora, minuto)
        self.warning_minutes: int = 5
        self.warning_callback: Optional[Callable[[int], None]] = None
        self.trigger_callback: Optional[Callable[[], None]] = None
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._warned_today: set = set()
        self._triggered_today: set = set()
        self._last_day: int = -1

    def set_schedules(self, schedules: List[Tuple[int, int]]) -> None:
        """Define os horários diários de disparo (lista de tuplas (hora, minuto))."""
        self.schedules = schedules

    def set_warning_lead_time(self, minutes: int) -> None:
        """Define com quantos minutos de antecedência o aviso prévio deve ser emitido."""
        self.warning_minutes = minutes

    def set_callbacks(
        self,
        trigger_callback: Callable[[], None],
        warning_callback: Optional[Callable[[int], None]] = None,
    ) -> None:
        """Registra os callbacks de disparo do quiz e de aviso prévio."""
        self.trigger_callback = trigger_callback
        self.warning_callback = warning_callback

    def start(self) -> None:
        """Inicia a thread do agendador."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="RaffSchedulerThread")
        self._thread.start()

    def stop(self) -> None:
        """Interrompe a thread do agendador."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    def is_running(self) -> bool:
        return self._running

    def _loop(self) -> None:
        while self._running:
            now = datetime.now()
            today_day = now.day

            # Reseta flags diárias ao mudar de dia
            if today_day != self._last_day:
                self._warned_today.clear()
                self._triggered_today.clear()
                self._last_day = today_day

            now_total_minutes = now.hour * 60 + now.minute

            for h, m in self.schedules:
                target_total_minutes = h * 60 + m
                schedule_key = (today_day, h, m)

                # Verifica aviso prévio
                warn_time_minutes = target_total_minutes - self.warning_minutes
                if (
                    now_total_minutes >= warn_time_minutes
                    and now_total_minutes < target_total_minutes
                    and schedule_key not in self._warned_today
                ):
                    self._warned_today.add(schedule_key)
                    if self.warning_callback:
                        remaining = target_total_minutes - now_total_minutes
                        try:
                            self.warning_callback(remaining)
                        except Exception:
                            pass

                # Verifica disparo do Quiz
                if (
                    now_total_minutes >= target_total_minutes
                    and schedule_key not in self._triggered_today
                ):
                    self._triggered_today.add(schedule_key)
                    if self.trigger_callback:
                        try:
                            self.trigger_callback()
                        except Exception:
                            pass

            # Dorme pelo intervalo de checagem
            for _ in range(self.check_interval_seconds):
                if not self._running:
                    break
                time.sleep(1)


# Instância singleton global do scheduler
_global_scheduler: Optional[RaffScheduler] = None

def get_scheduler() -> RaffScheduler:
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = RaffScheduler()
    return _global_scheduler
