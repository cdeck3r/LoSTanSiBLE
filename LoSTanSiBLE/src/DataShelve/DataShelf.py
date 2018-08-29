
import ntpath
import shelve
import pandas as pd


class DataShelf:
    """ DataShelf stores various records in a shelve / pickles structure.

        The DataShelf keeps an internal default DataFrame which is
        cumulatively updated when new records come in using the
        put_in_shelf(..) method. At each update the entire DataFrame
        is persisted in the shelf's file.

        The default DataFrame is stored under the shelf's filename as key
        in the shelf file.

    """

    # private class variables
    # we make explicit how the internal df looks like
    __df = pd.DataFrame(columns=['type', 'key', 'val','filename'])
    shelf_filepath = ''

    @classmethod
    def __init_internal_df(cls):
        cls.__df = pd.DataFrame(columns=['type', 'key', 'val','filename'])

    @classmethod
    def __shelf_name(cls):
        return ntpath.basename(cls.shelf_filepath)

    @classmethod
    def clear_shelf(cls, clearfile=False):
        """ The internal default dataframe will be emptied.

            This is useful when a previous records shall be removed
            before a new records is put in the shelf.

            :param clearfile: if true, clears the shelf file, too

        """
        cls.__init_internal_df()
        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            s.sync()
            s[cls.__shelf_name()] = cls.__df

        if clearfile:
            cls.clear_shelf_file()

    @classmethod
    def clear_shelf_file(cls, clearshelf=True):
        """ Clears whatever is in the shelf file.

            :param clearshelf: clears the content of the internal dataframe, too

        """
        #
        if len(cls.shelf_filepath) > 0:
            with shelve.open(cls.shelf_filepath, writeback=False) as s:
                s.sync()
                s.clear()
                if clearshelf:
                    cls.__init_internal_df()

                s[cls.__shelf_name()] = cls.__df

    @classmethod
    def put_in_shelf(cls, key, val, type='record'):
        """ Puts a new record in shelfself.

            The (key, val, type) are compiled into a dataframe.
            Afterwards, the frame is put into the shelf.

            :param key: descriptor for the value
            :param val: value to add
            :param type: set a type descriptor, default: record

        """
        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            d = {'type': type, 'key': key, 'val': val, 'filename': cls.__shelf_name()}
            row = pd.DataFrame(data=d, index=[0])
            cls.__df=cls.__df.append(row, sort=True, ignore_index=True)
            #cls.__df.reset_index(inplace=True)
            s[cls.__shelf_name()] = cls.__df

    @classmethod
    def put_in_shelf_df(cls, key, df):
        """ Puts an entire dataframe in the DataShelf.

            :param key: key to locate the dataframe in the shelf
            :param df: dataframe to be shelved

        """
        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            s[key] = df

    @classmethod
    def get_from_shelf(cls):
        """ Returns the default dataframe from shelf.

            :return: dataframe
        """
        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            return s[cls.__shelf_name()]

    @classmethod
    def get_from_shelf_df(cls, key):
        """ Return the dataframe identified by key.

            :param key: key to locate the dataframe in the shelf

            :return: dataframe
        """
        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            return s[key]

    @classmethod
    def indexlist(cls):
        """ Returns a list of all keys in the shelf.

            :return: list of keys

        """

        with shelve.open(cls.shelf_filepath, writeback=False) as s:
            return list(s.keys())
