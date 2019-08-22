import queue
import unittest
from unittest.mock import Mock

from server.action import Action, STATUS, NOT_FOUND


class TestAction(unittest.TestCase):

    def test_get_task_id(self):
        action = Action()
        action.task.clear()
        self.assertEqual('task_1', action.get_task_id())

        task_data = dict(cmd='reverse', string='test123')
        action.add_task(task_data)
        self.assertEqual('task_2', action.get_task_id())
        action.task.clear()

    def test_add_task(self):
        action = Action()
        queue.Queue.put = Mock()

        task_data = dict(cmd='reverse', string='test123')
        task_id = action.add_task(task_data)

        self.assertEqual(1, len(action.task))
        self.assertEqual('task_1', task_id)
        action.queue.put.assert_called_once_with(task_data)

        print(action.task)

    def test_get_status(self):
        action = Action()

        task_id = 'task_1'
        task = dict(cmd='reverse', string='test123', status=STATUS.queued)
        action.task[task_id].update(task)
        self.assertEqual(STATUS.queued.value, action.get_status(task_id))

        task.update(dict(status=STATUS.progress))
        action.task[task_id].update(task)
        self.assertEqual(STATUS.progress.value, action.get_status(task_id))

        task.update(dict(status=STATUS.complete))
        action.task[task_id].update(task)
        self.assertEqual(STATUS.complete.value, action.get_status(task_id))

    def test_get_result(self):
        action = Action()

        task_id = 'task_1'
        task = dict(cmd='reverse', string='test123', status=STATUS.queued)
        action.task[task_id].update(task)
        self.assertEqual(NOT_FOUND, action.get_result(task_id))

        task.update(dict(status=STATUS.progress))
        action.task[task_id].update(task)
        self.assertEqual(NOT_FOUND, action.get_result(task_id))

        task.update(dict(status=STATUS.complete, result='321tset'))
        action.task[task_id].update(task)
        self.assertEqual('321tset', action.get_result(task_id))

    def test_execute_action(self):
        action = Action()

        orig_reverse = Action.reverse
        orig_swap = Action.swap
        Action.reverse = Mock()
        Action.swap = Mock()

        params = dict(task_id='task_1', cmd='reverse', string='test123')
        action.execute_action(params)
        action.reverse.assert_called_once_with(params.get('string'))

        params = dict(task_id='task_2', cmd='swap', string='test123')
        action.execute_action(params)
        action.swap.assert_called_once_with(params.get('string'))

        Action.reverse = orig_reverse
        Action.swap = orig_swap

    def test_reverse(self):
        action = Action()
        action.SMALL_DELAY = 0

        init_str = 'abc'
        expected_str = 'cba'
        self.assertEqual(expected_str, action.reverse(init_str))

        init_str = 'testStringTestString2TestString3'
        expected_str = '3gnirtStseT2gnirtStseTgnirtStset'
        self.assertEqual(expected_str, action.reverse(init_str))

    def test_swap(self):
        action = Action()
        action.BIG_DELAY = 0

        init_str = 'abcd'
        expected_str = 'badc'
        self.assertEqual(expected_str, action.swap(init_str))

        init_str = 'abcdf'
        expected_str = 'badcf'
        self.assertEqual(expected_str, action.swap(init_str))


if __name__ == '__main__':
    unittest.main()
