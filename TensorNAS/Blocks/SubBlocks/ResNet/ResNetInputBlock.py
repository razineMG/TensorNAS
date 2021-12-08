from TensorNAS.Core.Block import Block


class Block(Block):

    from enum import Enum

    class SubBlocks(Enum):
        from enum import auto

        NONE = auto()

    def generate_constrained_input_sub_blocks(self, input_shape):
        from TensorNAS.Layers.Conv2D.Conv2D import Layer as Conv2D
        from TensorNAS.Layers.BatchNormalization import Layer as BatchNormalization
        from TensorNAS.Layers.Activation import Layer as Activation
        from TensorNAS.Layers.Pool.MaxPool2D import Layer as MaxPool2D
        from TensorNAS.Layers.Conv2D import Args as conv2d_args
        from TensorNAS.Layers.Pool import Args as pool_args
        from TensorNAS.Layers.Activation import Args as activation_args
        from TensorNAS.Core.Layer import ArgPadding
        from TensorNAS.Core.Layer import ArgRegularizers
        from TensorNAS.Core.Layer import ArgActivations

        layers = []

        layers.append(
            Conv2D(
                input_shape=input_shape,
                parent_block=self,
                args={
                    conv2d_args.FILTERS: 16,
                    conv2d_args.KERNEL_SIZE: (3, 3),
                    conv2d_args.STRIDES: (1, 1),
                    conv2d_args.PADDING: ArgPadding.SAME,
                    conv2d_args.KERNEL_REGULARIZER: (ArgRegularizers.L2, 1e-4),
                },
            )
        )
        layers.append(
            BatchNormalization(
                input_shape=layers[-1].get_output_shape(),
                parent_block=self,
            )
        )
        layers.append(
            Activation(
                input_shape=layers[-1].get_output_shape(),
                parent_block=self,
                args={activation_args.ACTIVATION: ArgActivations.RELU},
            )
        )
        # layers.append(
        #     MaxPool2D(
        #         input_shape=layers[-1].get_output_shape(),
        #         parent_block=self,
        #         args={pool_args.POOL_SIZE: (2, 2)},
        #     )
        # )

        return layers
