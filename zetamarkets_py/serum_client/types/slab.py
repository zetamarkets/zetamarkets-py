from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from construct import Container, Padding, Switch
from solders.pubkey import Pubkey


@dataclass
class SlabHeader:
    layout: typing.ClassVar = borsh.CStruct(
        "bump_index" / borsh.U32,
        "padding_1" / Padding(4),
        "free_list_length" / borsh.U32,
        "padding_2" / Padding(4),
        "free_list_head" / borsh.U32,
        "root" / borsh.U32,
        "leaf_count" / borsh.U32,
        "padding_3" / Padding(4),
    )
    bump_index: int
    free_list_length: int
    free_list_head: int
    root: int
    leaf_count: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SlabHeader":
        return cls(
            bump_index=obj.bump_index,
            free_list_length=obj.free_list_length,
            free_list_head=obj.free_list_head,
            root=obj.root,
            leaf_count=obj.leaf_count,
        )


# Different node types, we pad it all to size of 68 bytes.
UNINTIALIZED = borsh.CStruct("padding" / borsh.U8[68])
FREE_NODE = borsh.CStruct("next" / borsh.U32, "padding" / borsh.U8[64])
LAST_FREE_NODE = borsh.CStruct("padding" / borsh.U8[68])

# Used as dummy value for SlabNode#next.
NONE_NEXT = -1


@dataclass
class SlabInnerNode:
    layout: typing.ClassVar = borsh.CStruct(
        "prefix_len" / borsh.U32, "key" / borsh.U128, "children" / borsh.U32[2], "padding" / borsh.U8[40]
    )
    prefix_len: int
    key: int
    children: list[int]
    is_initialized: bool = True
    next: int = NONE_NEXT

    @classmethod
    def from_decoded(cls, obj: Container) -> "SlabInnerNode":
        return cls(
            prefix_len=obj.prefix_len,
            key=obj.key,
            children=obj.children,
        )


@dataclass
class SlabLeafNode:
    layout: typing.ClassVar = borsh.CStruct(
        "owner_slot" / borsh.U8,
        "fee_tier" / borsh.U8,
        "tif_offset" / borsh.U16,
        "key" / borsh.U128,
        "owner" / BorshPubkey,
        "quantity" / borsh.U64,
        "client_order_id" / borsh.U64,
    )
    owner_slot: int
    fee_tier: int
    tif_offset: int
    key: int
    owner: Pubkey
    quantity: int
    client_order_id: int
    is_initialized: bool = True
    next: int = NONE_NEXT

    @classmethod
    def from_decoded(cls, obj: Container) -> "SlabLeafNode":
        return cls(
            owner_slot=obj.owner_slot,
            fee_tier=obj.fee_tier,
            tif_offset=obj.tif_offset,
            key=obj.key,
            owner=obj.owner,
            quantity=obj.quantity,
            client_order_id=obj.client_order_id,
        )


@dataclass
class SlabNode:
    layout: typing.ClassVar = borsh.CStruct(
        "tag" / borsh.U32,
        "node"
        / Switch(
            lambda this: this.tag,
            {
                0: UNINTIALIZED,
                1: SlabInnerNode.layout,
                2: SlabLeafNode.layout,
                3: FREE_NODE,
                4: LAST_FREE_NODE,
            },
        ),
    )
    is_initialized: bool
    next: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SlabNode" | SlabInnerNode | SlabLeafNode:
        if obj.tag == 0:
            return cls(is_initialized=False, next=NONE_NEXT)
        elif obj.tag == 1:
            return SlabInnerNode.from_decoded(obj.node)
        elif obj.tag == 2:
            return SlabLeafNode.from_decoded(obj.node)
        elif obj.tag == 3:
            return cls(is_initialized=True, next=obj.node.next)
        elif obj.tag == 4:
            return cls(is_initialized=True, next=NONE_NEXT)
        else:
            raise RuntimeError("Invalid tag!")


@dataclass
class Slab:
    layout: typing.ClassVar = borsh.CStruct(
        "header" / SlabHeader.layout, "nodes" / SlabNode.layout[lambda this: this.header.bump_index]
    )
    header: SlabHeader
    nodes: list[SlabNode | SlabInnerNode | SlabLeafNode]

    @classmethod
    def from_decoded(cls, obj: Container) -> "Slab":
        return cls(
            header=SlabHeader.from_decoded(obj.header),
            nodes=list(
                map(
                    lambda item: SlabNode.from_decoded(item),
                    obj.nodes,
                )
            ),
        )

    def __iter__(self) -> typing.Iterable[SlabLeafNode]:
        return self.items(False)

    def items(self, descending=False) -> typing.Iterable[SlabLeafNode]:
        """Depth first traversal of the Binary Tree.
        Parameter descending decides if the price should descending or not.
        """
        if self.header.leaf_count == 0:
            return
        stack = [self.header.root]
        while stack:
            index = stack.pop()
            node: SlabNode | SlabInnerNode | SlabLeafNode = self.nodes[index]
            if isinstance(node, SlabLeafNode):
                yield node
            elif isinstance(node, SlabInnerNode):
                if descending:
                    stack.append(node.children[0])
                    stack.append(node.children[1])
                else:
                    stack.append(node.children[1])
                    stack.append(node.children[0])
            else:
                raise RuntimeError("Neither of leaf node or tree node!")
