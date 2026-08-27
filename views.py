import discord
from datetime import datetime

from ticket_manager import tickets, find_ticket_id, save_ticket, undo_ticket_step
from templates import (
    GREETING_TEMPLATE,
    MANDARIN_GREETING_TEMPLATE,
    NORMAL_DONE_TEMPLATE,
    MANDARIN_NORMAL_DONE_TEMPLATE,
    EXCLUDED_DONE_TEMPLATE,
    MANDARIN_EXCLUDED_DONE_TEMPLATE,
    CANCEL_REROUTE_TEMPLATE,
    CANCEL_ONSITE_TEMPLATE,
    CANCEL_DUPLICATE_TEMPLATE,
    CANCEL_ALREADY_IN_TARGET_TEMPLATE,
    CANCEL_SF_DISPLAY_BUG_TEMPLATE,
    CANCEL_WAITING_AUTHOR_3DAYS_TEMPLATE,
    CANCEL_MASTER_NOT_CORE_CLASS_TEMPLATE,
    CANCEL_BAD_STATUS_TEMPLATE,
    CANCEL_MULTI_SOURCE_SKU_TEMPLATE,
    ON_HOLD_GENERAL_TEMPLATE,
    ON_HOLD_UNLOCATED_SKU_TEMPLATE,
    ON_HOLD_IH_SRB_FSB_TEMPLATE,
    ON_HOLD_IH_APPROVAL_TEMPLATE,
    ON_HOLD_ENGINEERING_BUG_TEMPLATE,
    ON_HOLD_TOOL_ERROR_TEMPLATE,
    ON_HOLD_SPECIFIC_COLLECTION_TEMPLATE,
    ON_HOLD_BRAND_CHANGE_TEMPLATE,
    ON_HOLD_TARGET_COLLECTION_INFO_TEMPLATE,
    ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE,
    ON_HOLD_VAULT_PARTIAL_WHITE_LABEL_TEMPLATE,
    ON_HOLD_VAULT_COLLECTION_UPDATE_TEMPLATE,
    ON_HOLD_VAULT_UN_WHITE_LABEL_TEMPLATE,
)


# ============================================================
# HELPERS
# ============================================================

def progress(ticket):
    t_type = ticket.get("ticket_type")
    if t_type in ("cancel", "on_hold"):
        steps = [
            bool(ticket.get("assign")),
            bool(ticket.get("pending")),
            bool(ticket.get("greeting")),
            bool(ticket.get("done_comment")),
            bool(ticket.get("hours")),
            bool(ticket.get("done_done")),
        ]
    else:
        steps = [
            bool(ticket.get("assign")),
            bool(ticket.get("pending")),
            bool(ticket.get("greeting")),
            bool(ticket.get("com")),
            bool(ticket.get("done_comment")),
            bool(ticket.get("hours")),
            bool(ticket.get("done_done")),
        ]

    return int(sum(steps) / len(steps) * 100)


def progress_bar(value):
    total = 10
    filled = round(value / 100 * total)
    return "█" * filled + "░" * (total - filled)


def status_text(status):
    if status == "not_started":
        return "🟡 NOT STARTED"
    if status == "in_progress":
        return "🔵 IN PROGRESS"
    if status == "done":
        return "🟢 DONE"
    if status == "cancelled":
        return "🔴 CANCELLED"
    if status == "on_hold":
        return "🟠 PAUSED (Waiting for Supplier / Approval)"
    return status


def status_color(status):
    if status == "done":
        return discord.Color.green()
    if status == "cancelled":
        return discord.Color.red()
    if status == "on_hold":
        return discord.Color.orange()
    return discord.Color.blue()


def get_current_step(ticket):
    status = ticket.get("status")
    if status == "done":
        return "🟢 Done - Done (Completed)"
    if status == "cancelled":
        res = ticket.get("done_comment_type") or "Cancelled"
        return f"🔴 {res}"
    if status == "on_hold":
        res = ticket.get("done_comment_type") or "Paused"
        return f"🟠 {res}"
    if status == "not_started":
        return "🟡 Not Started"

    # In progress steps
    if not ticket.get("assign") or not ticket.get("pending"):
        return "▶ Start (Assign / Pending)"
    if not ticket.get("greeting"):
        return "💬 Greeting"

    t_type = ticket.get("ticket_type")
    if t_type == "cancel":
        if not ticket.get("done_comment"):
            return "🔴 Cancel Comment"
        if not ticket.get("hours"):
            return "⏱ Log Hours"
        return "🔴 Close Ticket"
    elif t_type == "on_hold":
        if not ticket.get("done_comment"):
            return "⏸️ On Hold Comment"
        if not ticket.get("hours"):
            return "⏱ Log Hours"
        return "⏸️ Pause Ticket"
    else:
        # DO workflow
        if not ticket.get("com"):
            return "📎 COM Submitted"
        if not ticket.get("done_comment"):
            return "💬 Done Comment"
        if not ticket.get("hours"):
            return "⏱ Log Hours"
        return "🟢 Done - Done"


def build_list_embed(filter_status=None):
    if not tickets:
        embed = discord.Embed(
            title="📋 Ticket Overview Dashboard",
            description="*Chưa có ticket nào trong hệ thống.*",
            color=discord.Color.light_grey()
        )
        return embed

    total = len(tickets)
    in_prog = sum(1 for t in tickets.values() if t.get("status") == "in_progress")
    paused = sum(1 for t in tickets.values() if t.get("status") == "on_hold")
    done = sum(1 for t in tickets.values() if t.get("status") == "done")
    cancelled = sum(1 for t in tickets.values() if t.get("status") == "cancelled")
    not_started = sum(1 for t in tickets.values() if t.get("status") == "not_started")

    embed = discord.Embed(
        title="📋 Ticket Overview Dashboard",
        description=(
            f"**Tổng số:** `{total}` tickets\n"
            f"🔵 In Progress: `{in_prog}` | 🟠 Paused: `{paused}` | 🟢 Done: `{done}` | 🔴 Cancelled: `{cancelled}` | 🟡 Not Started: `{not_started}`"
        ),
        color=discord.Color.blue()
    )

    filtered_tickets = {}
    for tid, t in tickets.items():
        st = t.get("status")
        if not filter_status or filter_status == "all":
            filtered_tickets[tid] = t
        elif filter_status == "in_progress" and st == "in_progress":
            filtered_tickets[tid] = t
        elif filter_status == "on_hold" and st == "on_hold":
            filtered_tickets[tid] = t
        elif filter_status == "done" and st == "done":
            filtered_tickets[tid] = t
        elif filter_status == "cancelled" and st == "cancelled":
            filtered_tickets[tid] = t

    if not filtered_tickets:
        embed.add_field(
            name="Kết quả lọc",
            value=f"*Không tìm thấy ticket nào với bộ lọc `{filter_status}`.*",
            inline=False
        )
        return embed

    for tid, t in list(filtered_tickets.items())[:25]:
        pct = progress(t)
        cur_step = get_current_step(t)
        lang = f" `{t['language']}`" if t.get("language") else ""
        extra_info = ""

        if t.get("status") == "on_hold":
            paused_time = t.get("completed_at") or t.get("created_at")
            if paused_time:
                from datetime import datetime
                diff = datetime.now() - paused_time
                days = diff.days
                hours = int(diff.total_seconds() // 3600) % 24
                if days >= 3:
                    extra_info = f"\n⚠️ **Đã dừng:** `{days} ngày {hours}h` *(Quá 3 ngày!)*"
                elif days >= 1:
                    extra_info = f"\n⏳ **Đã dừng:** `{days} ngày {hours}h`"
                else:
                    extra_info = f"\n⏳ **Đã dừng:** `{hours}h`"

        embed.add_field(
            name=f"🎫 #{tid}{lang}",
            value=f"👉 **Bước hiện tại:** `{cur_step}`\n📊 **Tiến độ:** {progress_bar(pct)} `{pct}%`{extra_info}",
            inline=False
        )

    return embed


def build_on_hold_reminder_embed():
    on_hold_tickets = {
        tid: t for tid, t in tickets.items() if t.get("status") == "on_hold"
    }

    if not on_hold_tickets:
        embed = discord.Embed(
            title="⏸️ Danh Sách Nhắc Nhở Ticket On Hold",
            description="🎉 **Không có ticket nào đang tạm dừng (On Hold)!**\nChúc bạn một ngày làm việc thuận lợi và hiệu quả!",
            color=discord.Color.green()
        )
        return embed

    total = len(on_hold_tickets)
    overdue_count = 0

    embed = discord.Embed(
        title="🔔 NHẮC NHỞ ĐẦU CA: Ticket On Hold Cần Kiểm Tra",
        description=(
            f"Chào buổi làm việc! Hiện có **`{total}`** ticket đang tạm dừng (On Hold).\n"
            f"💡 *Hãy kiểm tra lại phản hồi từ Supplier/Merchant để tiếp tục (`Resume`) hoặc hủy (`Cancel - 3 Days`).*"
        ),
        color=discord.Color.orange()
    )

    for tid, t in list(on_hold_tickets.items())[:25]:
        paused_time = t.get("completed_at") or t.get("created_at")
        days_str = ""
        is_overdue = False

        if paused_time:
            from datetime import datetime
            diff = datetime.now() - paused_time
            days = diff.days
            hours = int(diff.total_seconds() // 3600) % 24
            if days >= 3:
                is_overdue = True
                overdue_count += 1
                days_str = f"⚠️ **Đã dừng `{days} ngày {hours}h` (Quá hạn 3 ngày!)**"
            elif days >= 1:
                days_str = f"⏳ Đã dừng `{days} ngày {hours}h`"
            else:
                days_str = f"⏳ Đã dừng `{hours}h`"
        else:
            days_str = "⏳ Đang tạm dừng"

        reason = t.get("done_comment_type") or "On Hold"
        tip = " 👉 **Gợi ý:** Đã quá 3 ngày không phản hồi ➔ Có thể đóng ticket (`Cancel - 3 Days`)." if is_overdue else " 👉 Dùng `/status` để mở lại card tiếp tục."

        embed.add_field(
            name=f"🎫 #{tid} — {days_str}",
            value=f"📌 **Lý do:** `{reason}`\n{tip}",
            inline=False
        )

    if overdue_count > 0:
        embed.set_footer(text=f"⚠️ Có {overdue_count} ticket đã dừng >= 3 ngày cần kiểm tra xử lý gấp!")

    return embed


# ============================================================
# EMBED
# ============================================================

def build_embed(ticket_id):
    ticket_id = find_ticket_id(ticket_id)
    ticket = tickets[ticket_id]
    value = progress(ticket)

    assign = "☑" if ticket.get("assign") else "☐"
    pending = "☑" if ticket.get("pending") else "☐"
    greeting = "☑" if ticket.get("greeting") else "☐"
    com = "☑" if ticket.get("com") else "☐"
    done = "☑" if ticket.get("done_comment") else "☐"
    hours = "☑" if ticket.get("hours") else "☐"
    done_done = "☑" if ticket.get("done_done") else "☐"

    t_type = ticket.get("ticket_type")
    status = ticket.get("status")

    embed = discord.Embed(
        title=f"🎫 Ticket #{ticket_id}",
        description=(
            f"**Status:** {status_text(status)}\n\n"
            f"**Progress**\n"
            f"{progress_bar(value)} {value}%"
        ),
        color=status_color(status)
    )

    if status == "on_hold" or t_type == "on_hold":
        workflow_text = (
            f"{assign} Assign to me\n"
            f"{pending} Pending\n"
            f"{greeting} Greeting Comment\n"
            f"{done} On Hold Comment\n"
            f"{hours} Log Hours\n"
            f"{done_done} Paused (Waiting for Supplier)"
        )
    elif t_type == "cancel":
        workflow_text = (
            f"{assign} Assign to me\n"
            f"{pending} Pending\n"
            f"{greeting} Greeting Comment\n"
            f"{done} Cancel Comment\n"
            f"{hours} Log Hours\n"
            f"{done_done} Close Ticket"
        )
    else:
        workflow_text = (
            f"{assign} Assign to me\n"
            f"{pending} Pending\n"
            f"{greeting} Greeting Comment\n"
            f"{com} COM Submitted\n"
            f"{done} Done Comment\n"
            f"{hours} Log Hours\n"
            f"{done_done} Done - Done"
        )

    embed.add_field(name="Workflow", value=workflow_text, inline=False)

    if ticket.get("language"):
        lang_text = "🇨🇳 Mandarin" if ticket["language"] == "CN" else "🇺🇸 English"
        embed.add_field(
            name="Language",
            value=lang_text,
            inline=True
        )

    if ticket.get("done_comment_type"):
        embed.add_field(
            name="Resolution Type",
            value=ticket["done_comment_type"],
            inline=True
        )

    if ticket.get("completed_at"):
        embed.add_field(
            name="Completed",
            value=ticket["completed_at"].strftime("%Y-%m-%d %H:%M"),
            inline=True
        )

    if ticket.get("notes"):
        notes_text = "\n".join(f"• {note}" for note in ticket["notes"])
        embed.add_field(
            name="📝 Notes",
            value=notes_text[:1024],
            inline=False
        )

    return embed


# ============================================================
# DONE MODALS
# ============================================================

class ExcludedDoneModal(discord.ui.Modal):

    def __init__(self, ticket_id, is_mandarin: bool = False):
        title = "Mandarin Done - Excluded" if is_mandarin else "Normal Done - Excluded"
        super().__init__(title=title)
        self.ticket_id = find_ticket_id(ticket_id)
        self.is_mandarin = is_mandarin

        self.number = discord.ui.TextInput(
            label="Number of SKUs",
            placeholder="Example: 3",
            required=True
        )
        self.reason = discord.ui.TextInput(
            label="Reason",
            placeholder="Example: discontinued",
            required=True
        )

        self.add_item(self.number)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        ticket["ticket_type"] = "do"

        if self.is_mandarin:
            ticket["done_comment_type"] = "Mandarin Done - Excluded"
            template = MANDARIN_EXCLUDED_DONE_TEMPLATE
            title_text = "Mandarin Done - Excluded"
        else:
            ticket["done_comment_type"] = "Normal Done - Excluded"
            template = EXCLUDED_DONE_TEMPLATE
            title_text = "Normal Done - Excluded"

        text = template.format(
            number=self.number.value,
            reason=self.reason.value
        )

        await interaction.response.send_message(
            content=f"📋 **{title_text} — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="done"),
            ephemeral=True
        )


class DoneOtherModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Custom Done Comment")
        self.ticket_id = find_ticket_id(ticket_id)

        self.comment_type = discord.ui.TextInput(
            label="Resolution Name / Type",
            placeholder="Example: Done - Custom / Done with notes",
            default="Custom Done",
            required=True
        )
        self.comment_body = discord.ui.TextInput(
            label="Done Comment Text",
            placeholder="Enter full comment to post...",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.comment_type)
        self.add_item(self.comment_body)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        ticket["ticket_type"] = "do"
        ticket["done_comment_type"] = self.comment_type.value.strip() or "Custom Done"

        text = self.comment_body.value.strip()

        await interaction.response.send_message(
            content=f"📋 **{ticket['done_comment_type']} — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="done"),
            ephemeral=True
        )


# ============================================================
# CANCEL MODALS
# ============================================================

class DuplicateModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Cancel - Duplicate")
        self.ticket_id = find_ticket_id(ticket_id)

        self.original_ticket = discord.ui.TextInput(
            label="Original Ticket ID",
            placeholder="Example: ENRICH-1469000",
            required=True
        )
        self.add_item(self.original_ticket)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        orig_id = self.original_ticket.value.strip().upper()
        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"
        ticket["done_comment_type"] = f"Cancel - Duplicate ({orig_id})"

        text = CANCEL_DUPLICATE_TEMPLATE.format(original_ticket=orig_id)

        await interaction.response.send_message(
            content=f"📋 **Cancel - Duplicate — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel"),
            ephemeral=True
        )


class RerouteModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Cancel - Reroute")
        self.ticket_id = find_ticket_id(ticket_id)

        self.request_id = discord.ui.TextInput(
            label="Request ID / Short Title",
            placeholder="Example: Update SKU Attributes",
            required=True
        )
        self.target_team = discord.ui.TextInput(
            label="Target Team Name",
            placeholder="Example: Media Team / Pricing Team",
            required=True
        )
        self.update_details = discord.ui.TextInput(
            label="Action Requested / Details",
            placeholder="Detailed instructions for the target team",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.request_id)
        self.add_item(self.target_team)
        self.add_item(self.update_details)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        team_name = self.target_team.value.strip()
        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"
        ticket["done_comment_type"] = f"Cancel - Reroute ({team_name})"

        text = CANCEL_REROUTE_TEMPLATE.format(
            request_id=self.request_id.value.strip(),
            team_name=team_name,
            update_details=self.update_details.value.strip(),
            target_team=team_name,
            initial_update="DONE",
            summary=self.request_id.value.strip(),
            action_requested=self.update_details.value.strip(),
            next_steps="Execute request and complete or reroute"
        )

        await interaction.response.send_message(
            content=f"📋 **Cancel - Reroute — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel"),
            ephemeral=True
        )


class CancelAlreadyInTargetModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Already in Target Brand/Collection")
        self.ticket_id = find_ticket_id(ticket_id)

        self.sku = discord.ui.TextInput(
            label="SKU # [SKU #]",
            placeholder="Example: ABC1234, DEF5678",
            required=True
        )
        self.target_type = discord.ui.TextInput(
            label="Target Type",
            placeholder="Example: Target Brand or Target Collection",
            default="Target Brand",
            required=True
        )
        self.target_name = discord.ui.TextInput(
            label="Target Name (brand / collection)",
            placeholder="Example: Three Posts / Summer Collection",
            required=True
        )

        self.add_item(self.sku)
        self.add_item(self.target_type)
        self.add_item(self.target_name)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"
        ticket["done_comment_type"] = f"Cancel - Already in Target ({self.target_name.value.strip()})"

        text = CANCEL_ALREADY_IN_TARGET_TEMPLATE.format(
            sku=self.sku.value.strip(),
            target_type=self.target_type.value.strip(),
            target_name=self.target_name.value.strip()
        )

        await interaction.response.send_message(
            content=f"📋 **Cancel - Already in Target Brand/Collection — #{self.ticket_id}**\n*(📸 Lưu ý: Nhớ gửi kèm ảnh chụp màn hình minh chứng)*\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel"),
            ephemeral=True
        )


class CancelMultiSourceSkuModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Excluded from UnWL - Multi-Source")
        self.ticket_id = find_ticket_id(ticket_id)

        self.number = discord.ui.TextInput(
            label="Number of SKUs [x SKUs]",
            placeholder="Example: 2",
            required=True
        )
        self.add_item(self.number)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"
        ticket["done_comment_type"] = f"Cancel - Multi-Source SKUs ({self.number.value.strip()} SKUs)"

        text = CANCEL_MULTI_SOURCE_SKU_TEMPLATE.format(
            number=self.number.value.strip()
        )

        await interaction.response.send_message(
            content=f"📋 **Cancel - Excluded from UnWL (Multi-Source) — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel"),
            ephemeral=True
        )


class CancelOtherModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="Cancel - Other Reason")
        self.ticket_id = find_ticket_id(ticket_id)

        self.reason_name = discord.ui.TextInput(
            label="Reason Title / Summary",
            placeholder="Example: Cancel - Supplier Request / Invalid SKU",
            default="Cancel - Other",
            required=True
        )
        self.comment_body = discord.ui.TextInput(
            label="Cancel Comment Text",
            placeholder="Enter full comment to post...",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.reason_name)
        self.add_item(self.comment_body)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        r_name = self.reason_name.value.strip() or "Cancel - Other"
        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"
        ticket["done_comment_type"] = r_name

        text = self.comment_body.value.strip()

        await interaction.response.send_message(
            content=f"📋 **{r_name} — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel"),
            ephemeral=True
        )


# ============================================================
# ON HOLD MODALS
# ============================================================

class OnHoldUnlocatedSkuModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="On Hold - Không tìm thấy SKU")
        self.ticket_id = find_ticket_id(ticket_id)

        self.skus = discord.ui.TextInput(
            label="Part Numbers / SKUs",
            placeholder="Example: FRE146XXWHIT01, FRE146XXWHIT02...",
            style=discord.TextStyle.paragraph,
            required=True
        )
        self.supplier = discord.ui.TextInput(
            label="Supplier Name / Code",
            placeholder='Example: 1618 - Levinsohn Textile',
            required=True
        )

        self.add_item(self.skus)
        self.add_item(self.supplier)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        supplier_name = self.supplier.value.strip()
        ticket["ticket_type"] = "on_hold"
        ticket["status"] = "on_hold"
        ticket["done_comment_type"] = f"On Hold - Không tìm thấy SKU ({supplier_name})"

        text = ON_HOLD_UNLOCATED_SKU_TEMPLATE.format(
            skus=self.skus.value.strip(),
            supplier=supplier_name
        )

        await interaction.response.send_message(
            content=f"📋 **On Hold - Không tìm thấy SKU — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="on_hold"),
            ephemeral=True
        )


class EngineeringBugModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="On Hold - Engineering Bug")
        self.ticket_id = find_ticket_id(ticket_id)

        self.issue_summary = discord.ui.TextInput(
            label="Summary of Issue [XXXX]",
            placeholder="Example: Stuck Batch, Name Bank, tool freeze...",
            required=True
        )
        self.add_item(self.issue_summary)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        issue = self.issue_summary.value.strip()
        ticket["ticket_type"] = "on_hold"
        ticket["status"] = "on_hold"
        ticket["done_comment_type"] = f"On Hold - Engineering Bug ({issue})"

        text = ON_HOLD_ENGINEERING_BUG_TEMPLATE.format(issue_summary=issue)

        await interaction.response.send_message(
            content=f"📋 **On Hold - Engineering Bug — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="on_hold"),
            ephemeral=True
        )


class VaultOnHoldModal(discord.ui.Modal):

    def __init__(self, ticket_id, vault_key: str, vault_title: str):
        super().__init__(title=f"Vault: {vault_title[:40]}")
        self.ticket_id = find_ticket_id(ticket_id)
        self.vault_key = vault_key
        self.vault_title = vault_title

        self.recipient_name = discord.ui.TextInput(
            label="Recipient Name [insert name]",
            placeholder="Example: Supplier Team / John",
            default="Supplier Team",
            required=False
        )
        self.sku_list = discord.ui.TextInput(
            label="Priority SKU List [SKU list]",
            placeholder="Example: ABC1234, DEF5678, GHI9012...",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.recipient_name)
        self.add_item(self.sku_list)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        name = self.recipient_name.value.strip() or "Supplier Team"
        skus = self.sku_list.value.strip()

        is_are = "are" if ("," in skus or "\n" in skus or ";" in skus or " " in skus.strip()) else "is"

        templates_map = {
            "full_white_label": ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE,
            "partial_white_label": ON_HOLD_VAULT_PARTIAL_WHITE_LABEL_TEMPLATE,
            "collection_update": ON_HOLD_VAULT_COLLECTION_UPDATE_TEMPLATE,
            "un_white_label": ON_HOLD_VAULT_UN_WHITE_LABEL_TEMPLATE,
        }

        template_str = templates_map.get(self.vault_key, ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE)
        text = template_str.format(
            name=name,
            sku_list=skus,
            is_are=is_are
        )

        ticket["ticket_type"] = "on_hold"
        ticket["status"] = "on_hold"
        ticket["done_comment_type"] = f"On Hold - Vault: {self.vault_title}"

        await interaction.response.send_message(
            content=f"📋 **Vault: {self.vault_title} — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="on_hold"),
            ephemeral=True
        )


class OnHoldOtherModal(discord.ui.Modal):

    def __init__(self, ticket_id):
        super().__init__(title="On Hold - Other Reason")
        self.ticket_id = find_ticket_id(ticket_id)

        self.reason_name = discord.ui.TextInput(
            label="Reason Title / Summary",
            placeholder="Example: On Hold - Waiting for Merchant Review",
            default="On Hold - Other",
            required=True
        )
        self.comment_body = discord.ui.TextInput(
            label="On Hold Comment Text",
            placeholder="Enter full comment to post...",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.reason_name)
        self.add_item(self.comment_body)

    async def on_submit(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        r_name = self.reason_name.value.strip() or "On Hold - Other"
        ticket["ticket_type"] = "on_hold"
        ticket["status"] = "on_hold"
        ticket["done_comment_type"] = r_name

        text = self.comment_body.value.strip()

        await interaction.response.send_message(
            content=f"📋 **{r_name} — #{self.ticket_id}**\n\n```text\n{text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="on_hold"),
            ephemeral=True
        )


# ============================================================
# SUB-VIEWS
# ============================================================

class GreetingChoiceView(discord.ui.View):

    def __init__(self, ticket_id):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)

    @discord.ui.button(
        label="🇺🇸 English Greeting",
        style=discord.ButtonStyle.primary
    )
    async def english_greeting(self, interaction: discord.Interaction, button: discord.ui.Button):
        tickets[self.ticket_id]["language"] = "EN"
        await update_card(self.ticket_id, interaction.client)

        await interaction.response.edit_message(
            content=f"📋 **English Greeting — #{self.ticket_id}**\n\n```text\n{GREETING_TEMPLATE}\n```",
            embed=build_embed(self.ticket_id),
            view=GreetingPostedView(self.ticket_id)
        )

    @discord.ui.button(
        label="🇨🇳 Mandarin Greeting",
        style=discord.ButtonStyle.secondary
    )
    async def mandarin_greeting(self, interaction: discord.Interaction, button: discord.ui.Button):
        tickets[self.ticket_id]["language"] = "CN"
        await update_card(self.ticket_id, interaction.client)

        await interaction.response.edit_message(
            content=f"📋 **Mandarin Greeting — #{self.ticket_id}**\n\n```text\n{MANDARIN_GREETING_TEMPLATE}\n```",
            embed=build_embed(self.ticket_id),
            view=GreetingPostedView(self.ticket_id)
        )

    @discord.ui.button(
        label="⬅️ Quay lại",
        style=discord.ButtonStyle.secondary
    )
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


class GreetingPostedView(discord.ui.View):

    def __init__(self, ticket_id):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)

    @discord.ui.button(
        label="⬅️ Chọn lại Greeting",
        style=discord.ButtonStyle.secondary
    )
    async def rechoose(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="### 💬 Choose Greeting Language:",
            embed=build_embed(self.ticket_id),
            view=GreetingChoiceView(self.ticket_id)
        )

    @discord.ui.button(
        label="☑ Posted (Done)",
        style=discord.ButtonStyle.success
    )
    async def posted(self, interaction: discord.Interaction, button: discord.ui.Button):
        tickets[self.ticket_id]["greeting"] = True
        await update_card(self.ticket_id, interaction.client)

        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


class DoneCommentPostedView(discord.ui.View):

    def __init__(self, ticket_id, origin: str = "done"):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)
        self.origin = origin

    @discord.ui.button(
        label="⬅️ Chọn lại mẫu",
        style=discord.ButtonStyle.secondary
    )
    async def rechoose(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = tickets[self.ticket_id]
        if not ticket.get("done_comment"):
            ticket["done_comment_type"] = None
            if not ticket.get("com"):
                ticket["ticket_type"] = None

        if self.origin == "cancel":
            await interaction.response.edit_message(
                content="### 🔴 Choose Cancel Reason (No COM needed):",
                embed=build_embed(self.ticket_id),
                view=CancelOptionsView(self.ticket_id)
            )
        elif self.origin == "on_hold":
            await interaction.response.edit_message(
                content="### ⏸️ Choose On Hold Reason (No COM needed):",
                embed=build_embed(self.ticket_id),
                view=OnHoldOptionsView(self.ticket_id)
            )
        else:
            await interaction.response.edit_message(
                content="### 🟢 Choose Done Template:",
                embed=build_embed(self.ticket_id),
                view=DoneCommentView(self.ticket_id)
            )

    @discord.ui.button(
        label="☑ Posted (Done)",
        style=discord.ButtonStyle.success
    )
    async def posted(self, interaction: discord.Interaction, button: discord.ui.Button):
        tickets[self.ticket_id]["done_comment"] = True
        await update_card(self.ticket_id, interaction.client)

        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


class CancelSelect(discord.ui.Select):

    def __init__(self, ticket_id):
        self.ticket_id = find_ticket_id(ticket_id)
        options = [
            discord.SelectOption(
                label="Reroute",
                value="reroute",
                emoji="↪️",
                description="Chuyển tiếp ticket sang team khác (mở form)"
            ),
            discord.SelectOption(
                label="VĐ Onsite (Storefront Issue)",
                value="onsite",
                emoji="🌐",
                description="Lỗi storefront display trên web"
            ),
            discord.SelectOption(
                label="Duplicate Ticket",
                value="duplicate",
                emoji="📄",
                description="Trùng lặp với ticket khác (mở form)"
            ),
            discord.SelectOption(
                label="Already in Target Brand/Collection",
                value="already_in_target",
                emoji="🎯",
                description="SKU đã nằm đúng brand/collection (kèm ảnh minh chứng)"
            ),
            discord.SelectOption(
                label="Shop this Collection/Category Bug",
                value="sf_display_bug",
                emoji="🛒",
                description="Lỗi hiển thị replatformed SF display"
            ),
            discord.SelectOption(
                label="3 Days on Pause (Waiting for Author)",
                value="waiting_author_3days",
                emoji="⏳",
                description="Hết thời gian tạm dừng 3 ngày không phản hồi"
            ),
            discord.SelectOption(
                label="Master Class not Core Class",
                value="master_not_core",
                emoji="🚫",
                description="Master Class không thuộc Core Class của Exclusive Brands"
            ),
            discord.SelectOption(
                label="Bad Status (Not live on-site)",
                value="bad_status",
                emoji="⚠️",
                description="SKU không live on-site / Discontinued / Missing Imagery"
            ),
            discord.SelectOption(
                label="Excluded from UnWL (Multi-Source)",
                value="multi_source",
                emoji="❌",
                description="Không thực hiện được do sku set up Multi-Source (mở form)"
            ),
            discord.SelectOption(
                label="🏷️ Other / Lý do khác",
                value="other",
                emoji="🏷️",
                description="Nhập lý do và nội dung comment tùy chỉnh (mở form)"
            ),
        ]
        super().__init__(
            placeholder="🔽 Chọn lý do Cancel (hoặc Lý do khác)...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        val = self.values[0]

        if val == "reroute":
            await interaction.response.send_modal(RerouteModal(self.ticket_id))
            return
        elif val == "duplicate":
            await interaction.response.send_modal(DuplicateModal(self.ticket_id))
            return
        elif val == "already_in_target":
            await interaction.response.send_modal(CancelAlreadyInTargetModal(self.ticket_id))
            return
        elif val == "multi_source":
            await interaction.response.send_modal(CancelMultiSourceSkuModal(self.ticket_id))
            return
        elif val == "other":
            await interaction.response.send_modal(CancelOtherModal(self.ticket_id))
            return

        ticket["ticket_type"] = "cancel"
        ticket["status"] = "cancelled"

        templates_map = {
            "onsite": ("Cancel - VĐ Onsite", CANCEL_ONSITE_TEMPLATE),
            "sf_display_bug": ("Cancel - SF Display Bug", CANCEL_SF_DISPLAY_BUG_TEMPLATE),
            "waiting_author_3days": ("Cancel - Waiting for Author (3 Days)", CANCEL_WAITING_AUTHOR_3DAYS_TEMPLATE),
            "master_not_core": ("Cancel - Master Class not Core Class", CANCEL_MASTER_NOT_CORE_CLASS_TEMPLATE),
            "bad_status": ("Cancel - Bad Status (Not live)", CANCEL_BAD_STATUS_TEMPLATE),
        }

        type_name, template_text = templates_map[val]
        ticket["done_comment_type"] = type_name

        await interaction.response.edit_message(
            content=f"📋 **{type_name} — #{self.ticket_id}**\n\n```text\n{template_text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="cancel")
        )


class CancelOptionsView(discord.ui.View):
    """Dropdown selector with Cancel reasons + Back button"""

    def __init__(self, ticket_id):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)
        self.add_item(CancelSelect(ticket_id))

    @discord.ui.button(
        label="⬅️ Quay lại",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


class OnHoldSelect(discord.ui.Select):

    def __init__(self, ticket_id):
        self.ticket_id = find_ticket_id(ticket_id)
        options = [
            # Vault Category
            discord.SelectOption(
                label="🔒 Vault: Full White Label",
                value="vault_full_white_label",
                emoji="🔒",
                description="Priority list: Sort rank, PLAs, Brand, Description"
            ),
            discord.SelectOption(
                label="🔒 Vault: Partial White Label",
                value="vault_partial_white_label",
                emoji="🔒",
                description="Priority list: SKU brand change approval"
            ),
            discord.SelectOption(
                label="🔒 Vault: Collection Update (Same Brand)",
                value="vault_collection_update",
                emoji="🔒",
                description="Priority list: SKU collection update approval"
            ),
            discord.SelectOption(
                label="🔒 Vault: Un-White Label",
                value="vault_un_white_label",
                emoji="🔒",
                description="Priority list: Un-white label request approval"
            ),
            # Standard On Hold Category
            discord.SelectOption(
                label="📋 Xin list SKU (Chung)",
                value="general",
                emoji="📋",
                description="Yêu cầu cung cấp part numbers / SKUs chính xác"
            ),
            discord.SelectOption(
                label="🔍 Không tìm thấy SKU",
                value="unlocated",
                emoji="🔍",
                description="Điền SKUs & tên Supplier (mở popup form)"
            ),
            discord.SelectOption(
                label="👑 IH Approval - SRB/FSB",
                value="ih_srb_fsb",
                emoji="👑",
                description="Specialty Retail or Flagship brand merchant approval"
            ),
            discord.SelectOption(
                label="🏢 IH Approval Needed",
                value="ih_approval",
                emoji="🏢",
                description="Waiting for In-House team review"
            ),
            discord.SelectOption(
                label="🐛 Engineering Bug",
                value="eng_bug",
                emoji="🐛",
                description="Lỗi kỹ thuật / Stuck Batch / Name Bank (mở popup)"
            ),
            discord.SelectOption(
                label="🛠️ Tool Error",
                value="tool_error",
                emoji="🛠️",
                description="Waiting for engineering to fix tool-related issues"
            ),
            discord.SelectOption(
                label="🏷️ Specific Collection Name",
                value="collection_name",
                emoji="🏷️",
                description="Supplier yêu cầu tên Collection cụ thể"
            ),
            discord.SelectOption(
                label="🔄 Brand Change",
                value="brand_change",
                emoji="🔄",
                description="Supplier yêu cầu đổi Brand trong Exclusive Brands"
            ),
            discord.SelectOption(
                label="🎯 Target Collection / Brand Info",
                value="target_collection",
                emoji="🎯",
                description="Cần thêm thông tin SKU để xác định Target Collection"
            ),
            discord.SelectOption(
                label="🏷️ Other / Lý do khác",
                value="other",
                emoji="🏷️",
                description="Nhập lý do và nội dung tạm dừng tùy chỉnh (mở form)"
            ),
        ]
        super().__init__(
            placeholder="🔽 Chọn mẫu On Hold (hoặc Lý do khác)...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        ticket = tickets[self.ticket_id]
        val = self.values[0]

        # Vault Modals
        if val == "vault_full_white_label":
            await interaction.response.send_modal(
                VaultOnHoldModal(self.ticket_id, "full_white_label", "Full White Label")
            )
            return
        elif val == "vault_partial_white_label":
            await interaction.response.send_modal(
                VaultOnHoldModal(self.ticket_id, "partial_white_label", "Partial White Label")
            )
            return
        elif val == "vault_collection_update":
            await interaction.response.send_modal(
                VaultOnHoldModal(self.ticket_id, "collection_update", "Collection Update [SAME BRAND]")
            )
            return
        elif val == "vault_un_white_label":
            await interaction.response.send_modal(
                VaultOnHoldModal(self.ticket_id, "un_white_label", "Un-White Label")
            )
            return
        # Standard Modals
        elif val == "unlocated":
            await interaction.response.send_modal(OnHoldUnlocatedSkuModal(self.ticket_id))
            return
        elif val == "eng_bug":
            await interaction.response.send_modal(EngineeringBugModal(self.ticket_id))
            return
        elif val == "other":
            await interaction.response.send_modal(OnHoldOtherModal(self.ticket_id))
            return

        ticket["ticket_type"] = "on_hold"
        ticket["status"] = "on_hold"

        templates_map = {
            "general": ("On Hold - Xin list SKU", ON_HOLD_GENERAL_TEMPLATE),
            "ih_srb_fsb": ("On Hold - IH Approval (SRB/FSB)", ON_HOLD_IH_SRB_FSB_TEMPLATE),
            "ih_approval": ("On Hold - IH Approval Needed", ON_HOLD_IH_APPROVAL_TEMPLATE),
            "tool_error": ("On Hold - Tool Error", ON_HOLD_TOOL_ERROR_TEMPLATE),
            "collection_name": ("On Hold - Specific Collection Name", ON_HOLD_SPECIFIC_COLLECTION_TEMPLATE),
            "brand_change": ("On Hold - Brand Change", ON_HOLD_BRAND_CHANGE_TEMPLATE),
            "target_collection": ("On Hold - Target Collection Info", ON_HOLD_TARGET_COLLECTION_INFO_TEMPLATE),
        }

        type_name, template_text = templates_map[val]
        ticket["done_comment_type"] = type_name

        await interaction.response.edit_message(
            content=f"📋 **{type_name} — #{self.ticket_id}**\n\n```text\n{template_text}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="on_hold")
        )


class OnHoldOptionsView(discord.ui.View):
    """Dropdown selector with all On Hold templates (Vault + Standard) + Back button"""

    def __init__(self, ticket_id):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)
        self.add_item(OnHoldSelect(ticket_id))

    @discord.ui.button(
        label="⬅️ Quay lại",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


class DoneCommentView(discord.ui.View):
    """Done choices for tickets that completed work (after COM)"""

    def __init__(self, ticket_id):
        super().__init__(timeout=600)
        self.ticket_id = find_ticket_id(ticket_id)
        ticket = tickets[self.ticket_id]
        lang = ticket.get("language")

        if lang == "CN":
            btn_normal = discord.ui.Button(
                label="🇨🇳 Mandarin Done",
                style=discord.ButtonStyle.primary
            )
            btn_normal.callback = self.normal_done_cn

            btn_excluded = discord.ui.Button(
                label="🇨🇳 Mandarin Done - Excluded",
                style=discord.ButtonStyle.secondary
            )
            btn_excluded.callback = self.excluded_done_cn

            self.add_item(btn_normal)
            self.add_item(btn_excluded)

        else:
            btn_normal = discord.ui.Button(
                label="🇺🇸 Normal Done",
                style=discord.ButtonStyle.primary
            )
            btn_normal.callback = self.normal_done_en

            btn_excluded = discord.ui.Button(
                label="🇺🇸 Excluded Done",
                style=discord.ButtonStyle.secondary
            )
            btn_excluded.callback = self.excluded_done_en

            self.add_item(btn_normal)
            self.add_item(btn_excluded)

        btn_other = discord.ui.Button(
            label="📝 Other / Tùy chỉnh...",
            style=discord.ButtonStyle.secondary
        )
        btn_other.callback = self.done_other

        btn_back = discord.ui.Button(
            label="⬅️ Quay lại",
            style=discord.ButtonStyle.secondary
        )
        btn_back.callback = self.back_button

        self.add_item(btn_other)
        self.add_item(btn_back)

    async def normal_done_en(self, interaction: discord.Interaction):
        tickets[self.ticket_id]["ticket_type"] = "do"
        tickets[self.ticket_id]["done_comment_type"] = "Normal Done"

        await interaction.response.edit_message(
            content=f"📋 **Normal Done — #{self.ticket_id}**\n\n```text\n{NORMAL_DONE_TEMPLATE}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="done")
        )

    async def normal_done_cn(self, interaction: discord.Interaction):
        tickets[self.ticket_id]["ticket_type"] = "do"
        tickets[self.ticket_id]["done_comment_type"] = "Mandarin Done"

        await interaction.response.edit_message(
            content=f"📋 **Mandarin Done — #{self.ticket_id}**\n\n```text\n{MANDARIN_NORMAL_DONE_TEMPLATE}\n```",
            embed=build_embed(self.ticket_id),
            view=DoneCommentPostedView(self.ticket_id, origin="done")
        )

    async def excluded_done_en(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            ExcludedDoneModal(self.ticket_id, is_mandarin=False)
        )

    async def excluded_done_cn(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            ExcludedDoneModal(self.ticket_id, is_mandarin=True)
        )

    async def done_other(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            DoneOtherModal(self.ticket_id)
        )

    async def back_button(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content=None,
            embed=build_embed(self.ticket_id),
            view=TicketView(self.ticket_id)
        )


# ============================================================
# MAIN TICKET VIEW (CARD IN CHANNEL / STATUS)
# ============================================================

class TicketView(discord.ui.View):

    def __init__(self, ticket_id):
        super().__init__(timeout=None)
        self.ticket_id = find_ticket_id(ticket_id)
        self.update_buttons()

    def update_buttons(self):
        ticket = tickets[self.ticket_id]
        t_type = ticket.get("ticket_type")
        status = ticket.get("status")

        is_paused = (status == "on_hold")

        # Resume button (only enabled when ticket is on_hold / paused)
        self.resume_button.disabled = not is_paused

        # Standard buttons (disabled while paused so user clicks Resume first)
        self.start_button.disabled = (
            status != "not_started" or is_paused
        )

        self.greeting_button.disabled = (
            status == "not_started"
            or ticket["greeting"]
            or is_paused
        )

        # COM is only for DO workflow (bypassed if Cancel / On Hold)
        self.com_button.disabled = (
            not ticket["greeting"]
            or ticket["com"]
            or t_type in ("cancel", "on_hold")
            or ticket["done_comment"]
            or is_paused
        )

        # Done button is only enabled after COM
        self.done_button.disabled = (
            not ticket["com"]
            or ticket["done_comment"]
            or t_type in ("cancel", "on_hold")
            or is_paused
        )

        # Cancel and On Hold can be clicked right after Greeting (no COM required!)
        self.cancel_button.disabled = (
            not ticket["greeting"]
            or ticket["done_comment"]
            or ticket["com"]
            or is_paused
        )

        self.on_hold_button.disabled = (
            not ticket["greeting"]
            or ticket["done_comment"]
            or ticket["com"]
            or is_paused
        )

        # Hours: enabled as soon as done_comment is completed (for any workflow)
        self.hours_button.disabled = (
            not ticket["done_comment"]
            or bool(ticket.get("hours"))
        )

        # Action Button: adapt label and style based on ticket_type
        if is_paused or t_type == "on_hold":
            self.action_button.label = "⏸️ Pause Ticket"
            self.action_button.style = discord.ButtonStyle.secondary
            self.action_button.disabled = not (
                ticket["done_comment"]
                and bool(ticket.get("hours"))
                and not ticket.get("done_done")
            )
        elif t_type == "cancel":
            self.action_button.label = "🔴 Close (Cancelled)"
            self.action_button.style = discord.ButtonStyle.danger
            self.action_button.disabled = not (
                ticket["done_comment"]
                and bool(ticket.get("hours"))
                and not ticket.get("done_done")
            )
        else:
            self.action_button.label = "🟢 Done - Done"
            self.action_button.style = discord.ButtonStyle.success
            self.action_button.disabled = not (
                ticket["done_comment"]
                and bool(ticket.get("hours"))
                and not ticket.get("done_done")
            )

        # Undo button: enabled whenever any step has been started/progressed
        has_progress = bool(
            ticket.get("assign")
            or ticket.get("pending")
            or ticket.get("greeting")
            or ticket.get("com")
            or ticket.get("done_comment")
            or ticket.get("hours")
            or ticket.get("done_done")
            or status != "not_started"
        )
        self.undo_button.disabled = not has_progress

    # ========================================================
    # ROW 0: START -> GREETING -> COM -> RESUME
    # ========================================================

    @discord.ui.button(
        label="▶ Start",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = tickets[self.ticket_id]

        ticket["status"] = "in_progress"
        ticket["assign"] = True
        ticket["pending"] = True

        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)

    @discord.ui.button(
        label="💬 Greeting",
        style=discord.ButtonStyle.secondary,
        row=0
    )
    async def greeting_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="### 💬 Choose Greeting Language:",
            embed=build_embed(self.ticket_id),
            view=GreetingChoiceView(self.ticket_id),
            ephemeral=True
        )

    @discord.ui.button(
        label="📎 COM",
        style=discord.ButtonStyle.secondary,
        row=0
    )
    async def com_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = tickets[self.ticket_id]
        ticket["com"] = True
        ticket["ticket_type"] = "do"
        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)

    @discord.ui.button(
        label="▶ Resume",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = tickets[self.ticket_id]
        ticket["status"] = "in_progress"
        ticket["done_comment"] = False
        ticket["ticket_type"] = None
        ticket["done_done"] = False
        ticket["completed_at"] = None

        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)

    # ========================================================
    # ROW 1: 3 DECISION PATHS (DONE vs CANCEL vs ON HOLD)
    # ========================================================

    @discord.ui.button(
        label="💬 Done",
        style=discord.ButtonStyle.success,
        row=1
    )
    async def done_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="### 🟢 Choose Done Template:",
            embed=build_embed(self.ticket_id),
            view=DoneCommentView(self.ticket_id),
            ephemeral=True
        )

    @discord.ui.button(
        label="🔴 Cancel",
        style=discord.ButtonStyle.danger,
        row=1
    )
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="### 🔴 Choose Cancel Reason (No COM needed):",
            embed=build_embed(self.ticket_id),
            view=CancelOptionsView(self.ticket_id),
            ephemeral=True
        )

    @discord.ui.button(
        label="⏸️ On Hold",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def on_hold_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="### ⏸️ Choose On Hold Reason (No COM needed):",
            embed=build_embed(self.ticket_id),
            view=OnHoldOptionsView(self.ticket_id),
            ephemeral=True
        )

    # ========================================================
    # ROW 2: LOG HOURS, ACTION (DONE/CLOSE/PAUSE) & UNDO
    # ========================================================

    @discord.ui.button(
        label="⏱ Log Hours",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def hours_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        tickets[self.ticket_id]["hours"] = True
        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)

    @discord.ui.button(
        label="🟢 Done - Done",
        style=discord.ButtonStyle.success,
        row=2
    )
    async def action_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = tickets[self.ticket_id]

        ticket["done_done"] = True

        if ticket.get("ticket_type") == "on_hold":
            ticket["status"] = "on_hold"
            ticket["completed_at"] = datetime.now()
        elif ticket.get("ticket_type") == "cancel":
            ticket["status"] = "cancelled"
            ticket["completed_at"] = datetime.now()
        else:
            ticket["status"] = "done"
            ticket["completed_at"] = datetime.now()

        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)

    @discord.ui.button(
        label="↩️ Undo",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def undo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        success, msg = undo_ticket_step(self.ticket_id)
        self.update_buttons()

        await interaction.response.edit_message(
            embed=build_embed(self.ticket_id),
            view=self,
            content=None
        )
        await update_card(self.ticket_id, interaction.client)


# ============================================================
# UPDATE CARD
# ============================================================

async def update_card(ticket_id, bot):
    ticket_id = find_ticket_id(ticket_id)
    save_ticket(ticket_id)
    ticket = tickets.get(ticket_id)
    if not ticket or not ticket.get("channel_id") or not ticket.get("message_id"):
        return

    channel = bot.get_channel(ticket["channel_id"])
    if not channel:
        try:
            channel = await bot.fetch_channel(ticket["channel_id"])
        except Exception as e:
            print(f"[ERROR] Channel not found for #{ticket_id}: {e}")
            return

    try:
        message = await channel.fetch_message(ticket["message_id"])
        await message.edit(
            embed=build_embed(ticket_id),
            view=TicketView(ticket_id)
        )
    except Exception as e:
        print(f"[ERROR] Updating card #{ticket_id}: {e}")