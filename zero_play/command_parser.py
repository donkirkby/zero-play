import typing
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from inspect import getmembers
from itertools import count

from pkg_resources import iter_entry_points


class EntryPointArgument:
    def __init__(self, *args, **kwargs):
        """ Marks an attribute to be loaded from a command-line argument.

        Add one of these as a class attribute to an entry-point class, and the
        CommandParser will add a matching argument to the command line.
        Instances of the entry-point class will get assigned the matching value
        from the command line.
        :param args: passed to ArgumentParser.add_argument(), with
            '--name' added to the start, where name is the name of the
            attribute.
        :param kwargs: passed to ArgumentParser.add_argument()
        """
        self.args = args
        self.kwargs = kwargs


class CommandParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        """ Adds arguments based on entry point classes.

        The two features are to add arguments with the 'entry_point' action and
        to mark entry point classes with EntryPointArgument members.
        """
        super().__init__(*args, **kwargs)

        # {dest: {choice_name: entry_point}}
        self.entry_point_groups: typing.Dict[str,
                                             typing.Dict[str,
                                                         typing.Type]] = {}

        # {(dest, entry_name): [attr_dest]}
        self.entry_point_attrs: typing.Dict[
            typing.Tuple[str, str], typing.List[str]] = defaultdict(list)

    def add_argument(self, *args, **kwargs):
        """ Add arguments, including the 'entry_point' action.

        All the regular features are supported, but choices can be loaded from
        an entry point group if you use the 'entry_point' action. The entry
        point group will be 'zero_play.' plus the argument's name. The choices
        will be the entry point names, plus an extra number if there are
        duplicates.
        To load the chosen object from the entry point, call load_argument().
        """
        action = kwargs.get('action')
        if action == 'entry_point':
            kwargs['action'] = 'store'
        new_action = super(CommandParser, self).add_argument(*args, **kwargs)
        if action == 'entry_point':
            new_action.choices = sorted(self.load_group(new_action.dest))
        return new_action

    def load_argument(self,
                      namespace: Namespace,
                      dest: str,
                      entry_name: str = None,
                      **kwargs):
        """ Load the chosen object from an entry point.

        Creates an instance of the entry-point class, passing any marked
        attributes.
        :param namespace: the collection of arguments parsed from the command
            line.
        :param dest: the name of the argument to load from.
        :param entry_name: optional chosen value to load. This is useful when
            the argument accepts a list of values, and you want to load one of
            them.
        :param kwargs: passed along to the entry-point class's init method.
        """
        if entry_name is None:
            entry_name = getattr(namespace, dest)
        attrs = self.entry_point_attrs[(dest, entry_name)]
        for attr_name in attrs:
            kwargs[attr_name] = getattr(namespace, attr_name)
        entries = self.entry_point_groups[dest]
        entry_class = entries[entry_name]
        return entry_class(**kwargs)

    def load_group(self, dest: str):
        """ Load entry points from a group, making names unique.

        :param dest: the destination for the argument on the namespace.
            The entry point group will be zero_play.dest.
        """
        group_name = 'zero_play.' + dest
        entries: typing.Dict[str, typing.Type] = {}
        for entry_point in iter_entry_points(group_name):
            for i in count(1):
                entry_name = (entry_point.name
                              if i == 1
                              else f'{entry_point.name}-{i}')
                if entry_name not in entries:
                    entry_class = self.load_entry(dest, entry_name, entry_point)
                    entries[entry_name] = entry_class
                    break
        self.entry_point_groups[dest] = entries
        return entries

    def load_entry(self, dest, entry_name, entry_point):
        """ Load an entry-point class, and record extra arguments. """
        entry_class = entry_point.load()
        for member_name, member in getmembers(entry_class):
            if isinstance(member, EntryPointArgument):
                attrs = self.entry_point_attrs[(dest, entry_name)]
                attrs.append(member_name)
                option_string = '--' + member_name
                self.add_argument(option_string,
                                  *member.args,
                                  **member.kwargs)
        return entry_class
