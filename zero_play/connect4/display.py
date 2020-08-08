from zero_play.grid_display import GridDisplay, GraphicsPieceItem


class Connect4Display(GridDisplay):
    def calculate_move(self, row, column):
        return column

    def on_click(self, piece_item: GraphicsPieceItem):
        super().on_click(piece_item)
        # Display a preview of the move, if it's still available.
        self.on_hover_enter(piece_item)
